#!/usr/bin/env python3

"""Implement the denoising winer filter."""

from fractions import Fraction
import math
import typing

import torch

from cutcutcodec.core.classes.filter import Filter
from cutcutcodec.core.classes.frame_audio import FrameAudio
from cutcutcodec.core.classes.layout import Layout
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_audio import StreamAudio
from cutcutcodec.core.filter.audio.subclip import FilterAudioSubclip
from cutcutcodec.core.generation.audio.noise import GeneratorAudioNoise
from cutcutcodec.core.signal.psd import welch


class FilterAudioWiener(Filter):
    """Denoised a signal for a given stationary noise spectral density estimation.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.filter.audio.add import FilterAudioAdd
    >>> from cutcutcodec.core.filter.audio.equation import FilterAudioEquation
    >>> from cutcutcodec.core.filter.audio.subclip import FilterAudioSubclip
    >>> from cutcutcodec.core.filter.audio.wiener import FilterAudioWiener
    >>> from cutcutcodec.core.generation.audio.equation import GeneratorAudioEquation
    >>> from cutcutcodec.core.generation.audio.noise import GeneratorAudioNoise
    >>> _ = torch.manual_seed(0)
    >>> (noise,) = FilterAudioEquation(
    ...     GeneratorAudioNoise(0).out_streams,
    ...     "0.4*fl_0 + 0.2*sin(2*pi*100*t) + 0.1*sin(2*pi*200*t) + 0.1*sin(2*pi*400*t)",
    ...     "0.4*fr_0 + 0.2*cos(2*pi*100*t) + 0.1*cos(2*pi*200*t) + 0.1*cos(2*pi*400*t)",
    ... ).out_streams
    >>> (signal,) = GeneratorAudioEquation("0.5*sin(2*pi*440*t)", "0.5*cos(2*pi*440*t)").out_streams
    >>> (real_signal,) = FilterAudioAdd([signal, noise]).out_streams
    >>> (noise_slice,) = FilterAudioSubclip([noise], 0, 10).out_streams  # select the 10 first sec
    >>> (denoised,) = FilterAudioWiener([noise_slice, real_signal]).out_streams
    >>> frame_denoised = denoised.snapshot(10, 48000, 768000)
    >>> frame_signal = signal.snapshot(10, 48000, 768000)
    >>> torch.mean((frame_signal - real_signal.snapshot(10, 48000, 768000))**2)
    tensor(0.0834)
    >>> torch.mean((frame_signal - frame_denoised)**2)
    tensor(0.0148)
    >>>
    """

    def __init__(self, in_streams: typing.Iterable[StreamAudio]):
        """Initialise and create the class.

        Parameters
        ----------
        in_streams : typing.Iterable[StreamAudio]
            The concatenation of the noise stream and the audio streams to be denoised.
            Transmitted to ``cutcutcodec.core.classes.filter.Filter``.
        """
        super().__init__(in_streams, [_StreamAudioWiener(self)])
        noise = self.in_streams[0]
        assert isinstance(noise, StreamAudio), noise.__class__.__name__
        assert not math.isinf(noise.duration), "the noise stream has to be finite"

    def _getstate(self) -> dict:
        return {}

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert state == {}
        FilterAudioWiener.__init__(self, in_streams)

    @classmethod
    def default(cls):
        """Provide a minimalist example of an instance of this node."""
        return cls(FilterAudioSubclip(GeneratorAudioNoise.default, 0, 1).out_streams)


class _StreamAudioWiener(StreamAudio):
    """Denoise the audio streams."""

    def __init__(self, node: FilterAudioWiener):
        """Initialise and create the class.

        Parameters
        ----------
        node : cutcutcodec.core.filter.audio.wiener.FilterAudioWiener
            The node containing the StreamAudio to denoise.
        """
        assert isinstance(node, FilterAudioWiener), node.__class__.__name__
        super().__init__(node)
        self._psd_noise = {}

    def _get_psd_noise(self, rate: int) -> torch.Tensor:
        """Cache and compute the psd of the noise."""
        if rate not in self._psd_noise:
            noise_stream = self.node.in_streams[0]
            noise_frame = noise_stream.snapshot(
                noise_stream.beginning, rate, round(rate * noise_stream.duration)
            )
            self._psd_noise[rate] = welch(noise_frame)
        return self._psd_noise[rate]

    def _snapshot(self, timestamp: Fraction, rate: int, samples: int) -> FrameAudio:
        # get estimation of the noise psd (toto, set in cache to compute it only once)
        psd_noise = self._get_psd_noise(rate)
        # import matplotlib.pyplot as plt
        # plt.plot(psd_noise[0]); plt.show()

        # get raw signal
        raw = self.node.in_streams[1]._snapshot(timestamp, rate, samples)  # pylint: disable=W0212

        # overlapp add winer method
        out = FrameAudio(timestamp, rate, raw.layout, torch.zeros_like(raw))
        win = torch.signal.windows.hann(2*(psd_noise.shape[-1]-1))  # the sum of hanning is cst
        # import ipdb; ipdb.set_trace()
        for i in range(0, raw.shape[-1]-len(win)//2, len(win)//2):
            raw_slice = raw[..., i:i+len(win)]

            fft_raw_slice = torch.fft.rfft(raw_slice * win, norm="ortho", dim=-1)
            psd_raw = (fft_raw_slice.real**2 + fft_raw_slice.imag**2) / torch.sum(win)
            psd_src = torch.maximum(
                torch.tensor(1e-8, dtype=psd_raw.dtype, device=psd_raw.device), psd_raw - psd_noise
            )
            # import matplotlib.pyplot as plt
            # plt.plot(
            #     torch.fft.rfftfreq(len(win), 1/rate),
            #     psd_raw.T,
            #     label="psd noised signal",
            # )
            # plt.plot(
            #     torch.fft.rfftfreq(len(win), 1/rate),
            #     psd_src.T,
            #     label="estimation of psd source",
            # )
            # plt.legend()
            # plt.show()
            filter_h = (
                psd_src / (psd_src + psd_noise)
            )  # in frequency domain
            # filter_h = psd_src / psd_raw
            # print(filter_h)
            # import matplotlib.pyplot as plt
            # plt.plot(filter_h.T); plt.show()
            est_raw_slice = torch.fft.irfft(
                fft_raw_slice * filter_h,
                norm="ortho",
                dim=-1,
            )
            out[..., i:i+len(win)] += est_raw_slice.real

        # import matplotlib.pyplot as plt
        # plt.plot(out[0]); plt.show()

        return out

    @property
    def beginning(self) -> Fraction:
        return min(s.beginning for s in self.node.in_streams[1:])

    @property
    def duration(self) -> typing.Union[Fraction, float]:
        end = max(s.beginning + s.duration for s in self.node.in_streams[1:])
        return end - self.beginning

    @property
    def is_time_continuous(self) -> bool:
        """Return True if the data is continuous in the time domain, False if it is discrete."""
        if len(val := {s.is_time_continuous for s in self.node.in_streams[1:]}) != 1:
            raise AttributeError("combined streams are both time continuous and discrete")
        return val.pop()

    @property
    def layout(self) -> Layout:
        if len(layouts := {s.layout for s in self.node.in_streams[1:]}) != 1:
            raise AttributeError(f"add audio streams only implemented for same layout {layouts}")
        return layouts.pop()

#!/usr/bin/env python3

"""Tools for the Power Spectral Density (PSD) estimation."""

from fractions import Fraction
import numbers

import torch

from .window import dpss


def welch(signal: torch.Tensor, freq_resol: numbers.Real = None) -> torch.Tensor:
    """Estimate the power spectral density (PSD) with the Welch method.

    Parameters
    ----------
    signal : torch.Tensor
        The stationary signal on witch we evaluate the PSD.
        The tensor can be batched, so the shape is (..., n).
    freq_resol : float, default=10
        The norlised frequency resolution in Hz, assuming a sample rate of 1.
        It is the lowest denoised frequency as well.
        Higher it is, better is the resolution but noiser it is.

    Returns
    -------
    psd : torch.Tensor
        An estimation of the power spectral density, of shape (..., m).

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.signal.psd import welch
    >>> signal = torch.randn((32, 2, 768000))
    >>> psd = welch(signal)
    >>>
    >>> # freq = torch.fft.rfftfreq(2*psd.shape[-1]-1, 1/48000)
    >>> # import matplotlib.pyplot as plt
    >>> # _ = plt.plot(freq, psd[0].T)
    >>> # plt.show()
    >>>
    """
    assert isinstance(signal, torch.Tensor), signal.__class__.__name__
    freq_resol_min = Fraction(1, signal.shape[-1])  # theorical minimum frequency resolution
    if freq_resol is not None:
        assert isinstance(freq_resol, numbers.Real), freq_resol.__class__.__name__
        assert freq_resol >= freq_resol_min, f"you must provide freq_resol >= {freq_resol_min}"
    else:
        freq_resol = 2 * freq_resol_min
    win_len = min(2048, 2*round(0.5 / freq_resol))
    win = dpss(win_len, 5.0, dtype=signal.dtype)

    shift = win_len // 4  # should be choosen cleverer
    # if (exedent := (signal.shape[-1] - win_len) % shift) != 0:
    #     signal = signal[..., :-exedent]
    signal = signal.contiguous()
    # assert signal.is_contiguous(), "signal has to be C contiguous"
    psd = signal.as_strided(  # shape (..., o, m)
        (
            *signal.shape[:-1],
            (signal.shape[-1] - win_len) // shift + 1,  # number of slices
            win_len,
        ),
        (*signal.stride()[:-1], shift, 1),
    )
    psd = psd * win  # not inplace because blocs was not contiguous
    psd = torch.fft.rfft(psd, norm="ortho", dim=-1)
    psd = psd.real**2 + psd.imag**2
    psd = torch.mean(psd, dim=-2)  # shape (..., m)
    psd /= torch.sum(win)

    return psd

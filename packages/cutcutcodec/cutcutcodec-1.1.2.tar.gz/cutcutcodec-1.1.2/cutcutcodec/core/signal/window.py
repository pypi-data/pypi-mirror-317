#!/usr/bin/env python3

"""Window a signal to control gib effects.

The only window coded here is the optimal dpss window.
Thanks to its parameterization, it can be used in a general case to find the optimum compromise
between frequency accuracy and noise on secondary lob.
"""

import math
import numbers

import torch
import tqdm


def dpss(nb_samples: numbers.Integral, alpha: numbers.Real, dtype=torch.float64) -> torch.Tensor:
    """Compute the Discrete Prolate Spheroidal Sequences (DPSS).

    It is similar to the scipy function ``scipy.signal.windows.dpss``.

    Parameters
    ----------
    nb_samples : int
        The window size, it has to be >= 3.
    alpha : float
        Standardized half bandwidth.
    dtype : torch.dtype, default=float64
        The data type of the window samples: torch.float64 or torch.float32.

    Returns
    -------
    window : torch.Tensor
        The 1d symetric window, normalized with the maximum value at 1.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.signal.window import dpss
    >>> dpss(1024, 2.0, dtype=torch.float32)
    tensor([0.0166, 0.0172, 0.0177,  ..., 0.0177, 0.0172, 0.0166])
    >>>
    >>> # comparison with kaiser
    >>> alpha, nbr = 5.0, 129
    >>> win_dpss = dpss(nbr, alpha)
    >>> win_kaiser = torch.kaiser_window(
    ...     nbr, periodic=False, beta=alpha*torch.pi, dtype=torch.float64
    ... )
    >>> gain_dpss = 20*torch.log10(abs(torch.fft.rfft(win_dpss, 100000)))
    >>> gain_dpss -= torch.max(gain_dpss)
    >>> gain_kaiser = 20*torch.log10(abs(torch.fft.rfft(win_kaiser, 100000)))
    >>> gain_kaiser -= torch.max(gain_kaiser)
    >>>
    >>> # import matplotlib.pyplot as plt
    >>> # fig, (ax1, ax2) = plt.subplots(2)
    >>> # _ = ax1.plot(win_dpss, label="dpss")
    >>> # _ = ax1.plot(win_kaiser, label="kaiser")
    >>> # _ = ax1.legend()
    >>> # _ = ax2.plot(torch.linspace(0, 0.5, 50001), gain_dpss, label="dpss")
    >>> # _ = ax2.plot(torch.linspace(0, 0.5, 50001), gain_kaiser, label="kaiser")
    >>> # _ = ax2.axvline(x=alpha/nbr)
    >>> # _ = ax2.legend()
    >>> # plt.show()
    >>>
    """
    assert isinstance(nb_samples, numbers.Integral), nb_samples.__class__.__name__
    assert nb_samples >= 3, nb_samples
    assert isinstance(alpha, numbers.Real), alpha.__class__.__name__
    assert alpha > 0, alpha
    assert dtype in {torch.float32, torch.float64}, dtype
    # assert alpha >= 0.5*nb_samples, f"alpha={alpha} must be less than {nb_samples}/2"

    n_idx = torch.arange(nb_samples, dtype=dtype)
    diag = (0.5*(nb_samples - 1 - 2*n_idx))**2 * math.cos(2 * math.pi * float(alpha) / nb_samples)
    off_diag = 0.5 * n_idx[1:] * (nb_samples - n_idx[1:])

    # this step can be improved with 2 thinks:
    # 1) compute only the eigenvector of the last eigenvalue
    # 2) use the propertie the matrix is tridiagonal, not only hermitian
    matrix = torch.diag(diag)  # create a real symmetric tridiagonal matrix
    matrix[range(0, nb_samples-1), range(1, nb_samples)] = off_diag
    _, windows = torch.linalg.eigh(matrix, UPLO="U")
    window = windows[:, nb_samples-1].to(dtype)

    # normalisation
    if torch.sum(window) < 0:
        window *= -1
    window /= torch.amax(window)

    return window


def alpha_to_att(alpha: float) -> float:
    r"""Empirical estimation based on regression.

    The fitted model is \(attenuation = a*\alpha + b + c*tanh(d*\alpha)\).

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.signal.window import find_dpss_law
    >>> alphas, atts, _ = find_dpss_law()
    >>> alphas, atts = alphas.to(torch.float64), atts.to(torch.float64)
    >>> abcd = torch.tensor([26.54, 12.94, -22.85, 0.954], dtype=torch.float64, requires_grad=True)
    >>> optim = torch.optim.Adam([abcd])
    >>> for _ in range(10000):
    ...     pred = abcd[0]*alphas + abcd[1] + abcd[2]*torch.tanh(abcd[3]*alphas)
    ...     optim.zero_grad()
    ...     torch.mean((atts - pred)**2).backward()
    ...     optim.step()
    ...
    >>> abcd.detach().to(torch.float32)
    tensor([ 26.5422,  12.9422, -22.8484,   0.9542])
    >>> # import matplotlib.pyplot as plt
    >>> # _ = plt.plot(alphas.numpy(force=True), atts.numpy(force=True))
    >>> # _ = plt.plot(alphas.numpy(force=True), pred.numpy(force=True))
    >>> # plt.show()
    >>>
    """
    assert isinstance(alpha, float), alpha.__class__.__name__
    assert alpha >= 0, alpha
    cst_a = 26.542190409129383
    cst_b = 12.942220998411328
    cst_c = -22.84836385305482
    cst_d = 0.9542322385155504
    return cst_a*alpha + cst_b + cst_c*math.tanh(cst_d*alpha)


def alpha_to_band(alpha: float) -> float:
    r"""Empirical estimation based on regression.

    The fitted model is \(band = a*\alpha + b + c*tanh(d*\alpha)\).

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.signal.window import find_dpss_law
    >>> alphas, _, bands = find_dpss_law()
    >>> alphas, bands = alphas.to(torch.float64), bands.to(torch.float64)
    >>> abcd = torch.tensor([0.990, 0.807, -0.714, 1.194], dtype=torch.float64, requires_grad=True)
    >>> optim = torch.optim.Adam([abcd])
    >>> for _ in range(10000):
    ...     pred = abcd[0]*alphas + abcd[1] + abcd[2]*torch.tanh(abcd[3]*alphas)
    ...     optim.zero_grad()
    ...     torch.mean((bands - pred)**2).backward()
    ...     optim.step()
    ...
    >>> abcd.detach().to(torch.float32)
    tensor([ 0.9900,  0.8066, -0.7136,  1.1940])
    >>> # import matplotlib.pyplot as plt
    >>> # _ = plt.plot(alphas.numpy(force=True), bands.numpy(force=True))
    >>> # _ = plt.plot(alphas.numpy(force=True), pred.numpy(force=True))
    >>> # plt.show()
    >>>
    """
    assert isinstance(alpha, float), alpha.__class__.__name__
    assert alpha >= 0, alpha
    cst_a = 0.9899591248995603
    cst_b = 0.8066035087011443
    cst_c = -0.7135579410548559
    cst_d = 1.194021853577852
    return cst_a*alpha + cst_b + cst_c*math.tanh(cst_d*alpha)


def att_to_alpha(att: float) -> float:
    """Inverse of the empirical estimation based on regression.

    The inverse function is based on the tangent.

    Examples
    --------
    >>> from cutcutcodec.core.signal.window import alpha_to_att, att_to_alpha
    >>> round(alpha_to_att(att_to_alpha(20.0)), 4)
    20.0
    >>> round(alpha_to_att(att_to_alpha(40.0)), 4)
    40.0
    >>> round(alpha_to_att(att_to_alpha(80.0)), 4)
    80.0
    >>> round(alpha_to_att(att_to_alpha(120.0)), 4)
    120.0
    >>> round(alpha_to_att(att_to_alpha(160.0)), 4)
    160.0
    >>>
    """
    assert isinstance(att, float), att.__class__.__name__
    assert att >= 0.0, att
    b_min, b_max = 0.0, 1000.0
    f_min, f_max = alpha_to_att(b_min) - att, alpha_to_att(b_max) - att
    assert f_min <= 0 <= f_max, f"att {att} has to be in [{f_min+att}, {f_max+att}]"
    while b_max - b_min > 1e-10:
        # print(f"f({b_min})={f_min}, f({b_max})={f_max}")
        alpha = (b_min*f_max - b_max*f_min) / (f_max - f_min)
        if abs(f_inter := alpha_to_att(alpha) - att) < 1e-10:
            return alpha
        if f_inter > 0:
            b_max, f_max = alpha, f_inter
        else:
            b_min, f_min = alpha, f_inter
    return 0.5 * (b_min + b_max)


def find_dpss_law(
    nb_samples: numbers.Integral = 129,
    nb_alphas: numbers.Integral = 1000,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """For each beta parameter, associate the frequency properties.

    Parameters
    ----------
    nb_samples : int, default=129
        The window size, it has to be >= 3.
    nb_alphas : int, default=1000
        The number of alpha points.

    Returns
    -------
    alphas : torch.Tensor
        The apha values.
    atts : torch.Tensor
        The real positive attenuation of the secondaries lobs in dB.
    bands : torch.Tensor
        The normalised size of the main lob.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.signal.window import find_dpss_law
    >>> alphas, atts, bands = find_dpss_law()
    >>>
    >>> # import matplotlib.pyplot as plt
    >>> # _ = plt.plot(alphas.numpy(force=True), atts.numpy(force=True), label="attenuation")
    >>> # _ = plt.plot(alphas.numpy(force=True), bands.numpy(force=True), label="band")
    >>> # plt.legend()
    >>> # plt.show()
    >>>
    """
    assert isinstance(nb_samples, numbers.Integral), nb_samples.__class__.__name__
    assert nb_samples >= 3, nb_samples
    assert isinstance(nb_alphas, numbers.Integral), nb_alphas.__class__.__name__
    assert nb_alphas >= 1, nb_alphas

    alphas = torch.logspace(-2, 1, nb_alphas).tolist()
    atts = []  # attenuation in db
    bands = []  # band * nb_samples

    for alpha in tqdm.tqdm(alphas):
        win = dpss(nb_samples, alpha)
        gain = 20*torch.log10(abs(torch.fft.rfft(win, 200*nb_samples)))
        gain -= gain.max()
        idx = torch.argmax((gain[1:] > gain[:-1]).view(torch.uint8))
        att = -torch.max(gain[idx:])  # positive value
        band = torch.argmin(abs(gain[:idx] + att)) / 200
        atts.append(float(att))
        bands.append(float(band))

    return torch.asarray(alphas), torch.asarray(atts), torch.asarray(bands)

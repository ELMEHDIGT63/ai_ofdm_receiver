import numpy as np

def qam_modulate(bits, mod_order):
    """
    Modulate input bits using QAM (supports QPSK, 16QAM, etc.)
    Returns complex QAM symbols.
    """
    bits = np.array(bits)
    k = int(np.log2(mod_order))  # bits per symbol
    assert len(bits) % k == 0, "Bits length must be multiple of log2(M)"

    # Group bits into symbols
    bit_groups = bits.reshape((-1, k))

    # QPSK (4-QAM)
    if mod_order == 4:
        # Gray coding: 00->1+1j, 01->-1+1j, 11->-1-1j, 10->1-1j
        mapping = {
            (0, 0): 1 + 1j,
            (0, 1): -1 + 1j,
            (1, 1): -1 - 1j,
            (1, 0): 1 - 1j,
        }
        symbols = np.array([mapping[tuple(b)] for b in bit_groups])
        symbols /= np.sqrt(2)  # Normalize power to 1

    elif mod_order == 16:
        # Add later if needed
        raise NotImplementedError("Only QPSK (mod_order=4) is implemented.")

    else:
        raise ValueError("Unsupported modulation order")

    return symbols


def add_awgn(signal, snr_dB):
    """
    Add AWGN noise to signal at a given SNR (in dB).
    """
    signal_power = np.mean(np.abs(signal) ** 2)
    snr_linear = 10 ** (snr_dB / 10)
    noise_power = signal_power / snr_linear

    noise = np.sqrt(noise_power / 2) * (np.random.randn(*signal.shape) + 1j * np.random.randn(*signal.shape))
    return signal + noise
# Utility functions for BER, SNR calculations.

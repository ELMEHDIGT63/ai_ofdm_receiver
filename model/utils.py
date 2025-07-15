import numpy as np

def qam_modulate(bits, mod_order):
    """
    Modulate input bits using QAM (currently supports QPSK).
    """
    bits = np.array(bits)
    k = int(np.log2(mod_order))
    assert len(bits) % k == 0, "Bits length must be multiple of log2(M)"
    bit_groups = bits.reshape((-1, k))

    if mod_order == 4:
        # QPSK with Gray mapping
        mapping = {
            (0, 0): 1 + 1j,
            (0, 1): -1 + 1j,
            (1, 1): -1 - 1j,
            (1, 0): 1 - 1j,
        }
        symbols = np.array([mapping[tuple(b)] for b in bit_groups])
        symbols /= np.sqrt(2)  # Normalize power to 1
    else:
        raise NotImplementedError("Only QPSK supported.")

    return symbols


def qam_demodulate(symbols, mod_order):
    """
    Demodulate QAM symbols back to bit stream (QPSK only).
    """
    symbols *= np.sqrt(2)  # Denormalize
    bits = []
    for s in symbols:
        re, im = s.real, s.imag
        if re >= 0 and im >= 0:
            bits.extend([0, 0])
        elif re < 0 and im >= 0:
            bits.extend([0, 1])
        elif re < 0 and im < 0:
            bits.extend([1, 1])
        else:  # re >= 0 and im < 0
            bits.extend([1, 0])
    return np.array(bits, dtype=int)


def add_awgn(signal, snr_dB):
    """
    Add AWGN to a signal based on desired SNR in dB.
    """
    signal_power = np.mean(np.abs(signal) ** 2)
    snr_linear = 10 ** (snr_dB / 10)
    noise_power = signal_power / snr_linear
    noise = np.sqrt(noise_power / 2) * (np.random.randn(*signal.shape) + 1j * np.random.randn(*signal.shape))
    return signal + noise


# === Placeholder for Polar Encoding (3GPP-like) ===
def crc_append(bits, crc_len=24):
    """
    Append dummy CRC bits to payload (placeholder, not real CRC).
    """
    crc_bits = np.zeros(crc_len, dtype=int)  # For now: all 0s
    return np.concatenate([bits, crc_bits])

def polar_encode(bits, code_len):
    """
    Placeholder polar encoder. Just pad with 0s to match codeword length.
    """
    out = np.zeros(code_len, dtype=int)
    out[:len(bits)] = bits
    return out

from model.utils import qam_modulate, add_awgn, crc_append, polar_encode

def generate_sample():
    bits_per_symbol = int(np.log2(mod_order))
    total_bits = bits_per_packet

    # === Step 1: Generate payload bits ===
    payload_bits = np.random.randint(0, 2, total_bits)

    # === Step 2: Append CRC ===
    if use_crc:
        bits_with_crc = crc_append(payload_bits, crc_len=24)
    else:
        bits_with_crc = payload_bits

    # === Step 3: Polar encoding ===
    codeword = polar_encode(bits_with_crc, coded_bits)

    # === Step 4: QAM modulation ===
    num_symbols = len(codeword) // bits_per_symbol
    mod_symbols = qam_modulate(codeword[:num_symbols * bits_per_symbol], mod_order)

    # === Step 5: Superimpose pilots on active subcarriers ===
    tx_symbols = np.zeros(N_subcarriers, dtype=complex)
    pilot_symbols = np.ones(N_active_subcarriers, dtype=complex)

    # Power allocation
    data_part = mod_symbols[:N_active_subcarriers] * np.sqrt(1 - pilot_power_ratio)
    pilot_part = pilot_symbols * np.sqrt(pilot_power_ratio)
    combined = data_part + pilot_part

    # Insert into active subcarriers
    tx_symbols[np.array(active_indices)] = combined

    # === Step 6: IFFT to time domain ===
    tx_time = ifft(tx_symbols)

    # === Step 7: Multipath fading channel ===
    num_taps = np.random.choice(num_taps_range)
    doppler = np.random.choice(doppler_range_hz)
    h = generate_rayleigh_channel(num_taps, N_subcarriers, doppler)
    rx_time = convolve(tx_time, h, mode='same')

    # === Step 8: Add AWGN ===
    snr = np.random.choice(snr_dB)
    rx_time_noisy = add_awgn(rx_time, snr)

    # === Step 9: FFT back to frequency domain ===
    rx_freq = fft(rx_time_noisy)

    # === Step 10: Format input for AI (real + imag) ===
    X_sample = np.stack((rx_freq.real, rx_freq.imag), axis=-1)
    Y_sample = payload_bits  # Ground truth is original bits (before CRC and encoding)

    return X_sample, Y_sample

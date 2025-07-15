"""
generate_dataset.py

Generate OFDM symbols with superimposed pilots on active subcarriers
for URLLC short packets in a frequency-selective, time-varying channel.

Saves dataset for AI training.
"""

import numpy as np
from numpy.fft import ifft, fft
from scipy.signal import convolve
from ofdm_config import *
from model.utils import qam_modulate, add_awgn

def generate_rayleigh_channel(num_taps, N, doppler_hz):
    # Generate Rayleigh fading channel impulse response
    h = (np.random.randn(num_taps) + 1j * np.random.randn(num_taps)) / np.sqrt(2 * num_taps)
    delays = np.sort(np.random.randint(0, N//4, size=num_taps))
    channel = np.zeros(N, dtype=complex)
    channel[delays] = h
    # TODO: Add Doppler/time variation modeling if needed
    return channel

def generate_sample():
    bits_per_symbol = int(np.log2(mod_order))
    total_bits = bits_per_packet

    # Generate random payload bits
    bits = np.random.randint(0, 2, total_bits)

    # Placeholder: Insert your polar+CRC encoding here, for now treat bits as coded bits
    coded_bits = bits  # TODO: replace with encoded bits

    # Map coded bits to QAM symbols
    num_symbols = len(coded_bits) // bits_per_symbol
    mod_symbols = qam_modulate(coded_bits[:num_symbols * bits_per_symbol], mod_order)

    # Prepare full OFDM symbol array (all zero initially)
    tx_symbols = np.zeros(N_subcarriers, dtype=complex)

    # Place symbols only on active subcarriers
    tx_symbols[np.array(active_indices)] = mod_symbols[:N_active_subcarriers]

    # Generate known pilot symbols on active subcarriers
    pilot_symbols = np.ones(N_active_subcarriers, dtype=complex)

    # Apply power splitting
    data_part = tx_symbols[np.array(active_indices)] * np.sqrt(1 - pilot_power_ratio)
    pilot_part = pilot_symbols * np.sqrt(pilot_power_ratio)

    # Superimpose pilots on data
    tx_symbols[np.array(active_indices)] = data_part + pilot_part

    # IFFT to time domain
    tx_time = ifft(tx_symbols)

    # Channel modeling
    num_taps = np.random.choice(num_taps_range)
    doppler = np.random.choice(doppler_range_hz)
    h = generate_rayleigh_channel(num_taps, N_subcarriers, doppler)

    # Convolve transmitted signal with channel impulse response
    rx_time = convolve(tx_time, h, mode='same')

    # Add AWGN noise
    snr = np.random.choice(snr_dB)
    rx_time_noisy = add_awgn(rx_time, snr)

    # FFT back to frequency domain
    rx_freq = fft(rx_time_noisy)

    # Prepare input feature: stack real and imag parts
    X_sample = np.stack((rx_freq.real, rx_freq.imag), axis=-1)

    # Output label: original bits (before encoding ideally)
    Y_sample = bits

    return X_sample, Y_sample

def generate_dataset(split="train"):
    num = num_samples if split == "train" else num_samples // 4
    X_list, Y_list = [], []
    for _ in range(num):
        X, Y = generate_sample()
        X_list.append(X)
        Y_list.append(Y)

    X_arr = np.array(X_list)
    Y_arr = np.array(Y_list)

    np.savez(f"data/{split}_data.npz", X=X_arr, Y=Y_arr)
    print(f"{split} dataset saved: X={X_arr.shape}, Y={Y_arr.shape}")

if __name__ == "__main__":
    generate_dataset("train")
    generate_dataset("test")
# Generate synthetic dataset with OFDM blocks and labels.

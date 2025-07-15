# OFDM + Superimposed Pilot Configuration (Research-grade)

# === 3GPP/IEEE-based OFDM Parameters ===
N_subcarriers = 72  # 3GPP standard for mini-slot use
N_symbols_per_minislot = 2  # Can also be 4 or 7 depending on latency need

# === Modulation ===
mod_order = 4  # QPSK, corresponds to 2 bits per symbol

# === Pilot Power Ratio (will be tuned during testing) ===
# Pilot and data symbols share total Tx power budget
pilot_power_ratio = 0.1  # Try 0.1 or 0.2 (0.9/0.1, 0.8/0.2 split)

# === SNR Range (in dB) for training/testing ===
snr_dB = [0, 5, 10, 15, 20]  # Training and testing scenarios

# === Dataset Parameters ===
num_samples = 10000  # Total OFDM blocks to generate for dataset

# === Channel Model Parameters (3GPP compliant fading scenarios) ===
num_taps_range = [3, 5, 7, 10]  # Multipath tap variations (wide range)
doppler_range_hz = [5, 30, 100, 300]  # Doppler frequency (Hz) per 3GPP

# === Notes ===
# - Superimposed pilots must preserve total power budget.
# - Pilot = known_sequence * sqrt(alpha)
# - Data = modulated_data * sqrt(1 - alpha)
# - All channel models should follow 3GPP TR 38.901 and IEEE 802.11/15 style.
# OFDM system configuration parameters.

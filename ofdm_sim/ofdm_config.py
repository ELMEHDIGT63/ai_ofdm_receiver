# OFDM + Superimposed Pilot Configuration (Research-grade, URLLC focused)

# === 3GPP/IEEE-based OFDM Parameters ===
N_subcarriers = 72  # Total subcarriers in a mini-slot (3GPP)
N_active_subcarriers = 16  # Only 16 used to carry data/pilot
active_indices = list(range(28, 28 + N_active_subcarriers))  # Centered allocation (28-43)

N_symbols_per_minislot = 2  # Can also be 4 or 7 depending on latency constraints

# === Modulation ===
mod_order = 4  # QPSK, 2 bits per symbol

# === Pilot Power Ratio ===
pilot_power_ratio = 0.1  # Pilot/data split. Try sweeping 0.1 to 0.2

# === SNR Range for Simulation ===
snr_dB = [0, 5, 10, 15, 20]

# === Dataset Parameters ===
num_samples = 10000

# === Channel Model Parameters (3GPP-style multipath fading) ===
num_taps_range = [3, 5, 7, 10]  # Number of multipath taps

# Smooth Doppler spread range (Hz), from 0 to 300 Hz in 25 Hz steps
doppler_range_hz = list(range(0, 301, 25))

# === URLLC Short Packet Configuration ===
bits_per_packet = 100            # Payload size (bits)
coding_rate = 0.5                # Typical for URLLC
coded_bits = int(bits_per_packet / coding_rate)  # 200 coded bits
coding_scheme = "polar"          # 3GPP TS 38.212 mandated
use_crc = True                   # Add CRC before Polar encoding (24 bits typical)

# === Notes ===
# - Only `active_indices` subcarriers carry signal
# - Pilot = known_sequence * sqrt(alpha), Data = mod_data * sqrt(1 - alpha)
# - IFFT/FFT applied to full 72-subcarrier OFDM symbol
# - Channel and coding parameters follow 3GPP TR 38.901 and TS 38.212

# Script will plot astigmatis, defocus and record number collected on the Talos Arctica using serialEM
# It needs the serialEM log file as input
# this script by Dr. Joshua Strauss on 3/17/25 using Gemini

import matplotlib.pyplot as plt
import re
import numpy as np

def plot_astigm_defocus_record(filename, window_size=10):
    """Plots astigmatism and defocus vs. record number with moving average trend lines."""

    record_numbers = []
    astigmatism_values = []
    defocus_values = []

    try:
        with open(filename, 'r') as f:
            for line in f:
                record_match = re.search(r"taking record (\d+)", line)
                astig_match = re.search(r"astig: ([\d.]+)", line)
                defocus_match = re.search(r"defocus: (-?[\d.]+)", line)

                if record_match:
                    try:
                        record_numbers.append(int(record_match.group(1)))
                    except ValueError:
                        print(f"Warning: Invalid record number format in line: {line.strip()}")
                if astig_match:
                    try:
                        astigmatism_values.append(float(astig_match.group(1)))
                    except ValueError:
                        print(f"Warning: Invalid astigmatism value format in line: {line.strip()}")
                if defocus_match:
                    try:
                        defocus_values.append(float(defocus_match.group(1)))
                    except ValueError:
                        print(f"Warning: Invalid defocus value format in line: {line.strip()}")

        print(len(record_numbers), len(astigmatism_values), len(defocus_values))

        # Filter to keep only matching pairs
        paired_data = []
        min_length = min(len(record_numbers), len(astigmatism_values), len(defocus_values))
        for i in range(min_length):
            paired_data.append((record_numbers[i], astigmatism_values[i], defocus_values[i]))

        if paired_data:
            record_numbers_filtered, astigmatism_values_filtered, defocus_values_filtered = zip(*paired_data)
            record_numbers_filtered = np.array(record_numbers_filtered)
            astigmatism_values_filtered = np.array(astigmatism_values_filtered)
            defocus_values_filtered = np.array(defocus_values_filtered)

            # Astigmatism Plot
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.plot(record_numbers_filtered, astigmatism_values_filtered, 'o', label='Astigmatism')
            if len(astigmatism_values_filtered) >= window_size:
                astig_moving_average = np.convolve(astigmatism_values_filtered, np.ones(window_size)/window_size, mode='valid')
                astig_moving_average_record_numbers = record_numbers_filtered[window_size - 1:]
                plt.plot(astig_moving_average_record_numbers, astig_moving_average, '-', label=f'Moving Avg (window={window_size})')
            else:
                print(f"Warning: Not enough astigmatism data points to calculate moving average with window size {window_size}.")
            plt.xlabel("Record Number (Exposure)")
            plt.ylabel("Astigmatism (um)")
            plt.title("Astigmatism vs. Record Number")
            plt.grid(True)
            plt.legend()

            # Defocus Plot
            plt.subplot(1, 2, 2)
            plt.plot(record_numbers_filtered, defocus_values_filtered, 'o', label='Defocus')
            if len(defocus_values_filtered) >= window_size:
                defocus_moving_average = np.convolve(defocus_values_filtered, np.ones(window_size)/window_size, mode='valid')
                defocus_moving_average_record_numbers = record_numbers_filtered[window_size - 1:]
                plt.plot(defocus_moving_average_record_numbers, defocus_moving_average, '-', label=f'Moving Avg (window={window_size})')
            else:
                print(f"Warning: Not enough defocus data points to calculate moving average with window size {window_size}.")
            plt.xlabel("Record Number (Exposure)")
            plt.ylabel("Defocus (um)")
            plt.title("Defocus vs. Record Number")
            plt.grid(True)
            plt.legend()

            plt.tight_layout()
            plt.show()
        else:
            print("Error: No matching record number, astigmatism, and defocus data found.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

plot_astigm_defocus_record('/Users/cryoem_core1/PycharmProjects/plot_astig/20250315_log.log')
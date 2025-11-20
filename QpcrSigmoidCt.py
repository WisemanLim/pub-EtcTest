import numpy as np
import matplotlib.pyplot as plt
import os

NUM_CYCLES = 40
NUM_SAMPLES = 16

def sigmoid(cycle, Fmax, C_half, k):
    return Fmax / (1.0 + np.exp(-k * (cycle - C_half)))

def second_derivative(cycle, Fmax, C_half, k):
    h = 1e-2
    return (sigmoid(cycle + h, Fmax, C_half, k)
            - 2.0 * sigmoid(cycle, Fmax, C_half, k)
            + sigmoid(cycle - h, Fmax, C_half, k)) / (h * h)

def calculate_ct(Fmax, C_half, k):
    max_sdm = -np.inf
    ct = 0.0
    for c in np.arange(0.0, NUM_CYCLES, 0.1):
        sdm = second_derivative(c, Fmax, C_half, k)
        if sdm > max_sdm:
            max_sdm = sdm
            ct = c
    return ct

def estimate_efficiency(fluorescence, C1, C2):
    i1 = int(round(C1))
    i2 = int(round(C2))
    if i1 < 0 or i2 >= len(fluorescence) or i1 >= i2:
        return -1.0
    F1 = fluorescence[i1]
    F2 = fluorescence[i2]
    if F1 <= 0 or F2 <= 0:
        return -1.0
    return (pow(F2 / F1, 1.0 / (i2 - i1)) - 1.0)

def main():
    current_path = os.path.abspath('.')
    print(f"Current dir: {current_path}")
    # CSV 파일 읽기
    fluorescence_data = np.zeros((NUM_SAMPLES, NUM_CYCLES), dtype=float)
    with open(os.path.join(current_path, 'qpcr_input.csv')) as f:
        lines = f.readlines()
        # 첫 줄은 헤더
        for sample_idx, line in enumerate(lines[1:]):
            print(f"{sample_idx}: {line}")
            if sample_idx >= NUM_SAMPLES:
                break
            parts = line.strip().split(',')
            # 첫 번째 열은 cycle 번호이므로 무시
            for j in range(1, min(len(parts), NUM_CYCLES+1)):
                fluorescence_data[sample_idx, j-1] = float(parts[j])

    cycles = np.arange(NUM_CYCLES)
    plt.figure(figsize=(10, 7))
    for i in range(NUM_SAMPLES):
        fluorescence = fluorescence_data[i].copy()
        min_val = np.min(fluorescence)
        fluorescence -= min_val
        Fmax = np.max(fluorescence)
        C_half = 27.0
        k = 0.4
        Ct = calculate_ct(Fmax, C_half, k)
        efficiency = estimate_efficiency(fluorescence, Ct - 2, Ct + 2)
        fitted = [sigmoid(c, Fmax, C_half, k) for c in cycles]
        plt.plot(cycles, fitted, label=f'Tube {i+1} (Ct: {Ct:.2f})')
        print(f"Tube {i+1}: Ct = {Ct:.2f}, Efficiency = {efficiency:.2f} ({efficiency*100:.1f}%)")

    plt.title("qPCR Sigmoid Curves")
    plt.xlabel("Cycle")
    plt.ylabel("Fluorescence")
    plt.legend()
    plt.tight_layout()
    plt.savefig("qpcr_sigmoid_plot.png")
    plt.show()

if __name__ == "__main__":
    main()
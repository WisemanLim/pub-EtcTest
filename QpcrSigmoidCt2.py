import numpy as np
import matplotlib.pyplot as plt
import os

# CSV 파일 경로
current_path = os.path.abspath('.')
csv_path = os.path.join(current_path, 'qpcr_input.csv')

# CSV 파일에서 Tube 개수와 cycle 개수 동적 추출
with open(csv_path) as f:
    lines = f.readlines()
    header = lines[0].strip().split(',')
    tube_names = header[1:]  # 첫 번째 컬럼은 cycle
    NUM_SAMPLES = len(tube_names)
    NUM_CYCLES = len(lines) - 1  # 헤더 제외

print(f"Tube 개수(NUM_SAMPLES): {NUM_SAMPLES}")
print(f"Cycle 개수(NUM_CYCLES): {NUM_CYCLES}")

# 데이터 읽기
fluorescence_data = np.zeros((NUM_SAMPLES, NUM_CYCLES), dtype=float)
for cycle_idx, line in enumerate(lines[1:]):
    parts = line.strip().split(',')
    for tube_idx in range(NUM_SAMPLES):
        fluorescence_data[tube_idx, cycle_idx] = float(parts[tube_idx + 1])

cycles = np.arange(NUM_CYCLES)
plt.figure(figsize=(10, 7))

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
    plt.plot(cycles, fitted, label=f'{tube_names[i]} (Ct: {Ct:.2f})')
    print(f"{tube_names[i]}: Ct = {Ct:.2f}, Efficiency = {efficiency:.2f} ({efficiency*100:.1f}%)")

plt.title("qPCR Sigmoid Curves")
plt.xlabel("Cycle")
plt.ylabel("Fluorescence")
plt.legend()
plt.tight_layout()
plt.savefig("qpcr_sigmoid_plot.png")
plt.show()
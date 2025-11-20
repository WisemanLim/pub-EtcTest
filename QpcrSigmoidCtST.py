import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="qPCR Sigmoid Analysis", layout="wide")
st.title("qPCR Sigmoid Curve Analysis")

uploaded_file = st.file_uploader("qpcr_input.csv 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    tube_names = list(df.columns[1:])  # 첫 번째 컬럼은 cycle
    NUM_SAMPLES = len(tube_names)
    NUM_CYCLES = df.shape[0]
    st.write(f"Tube 개수(NUM_SAMPLES): {NUM_SAMPLES}")
    st.write(f"Cycle 개수(NUM_CYCLES): {NUM_CYCLES}")

    fluorescence_data = np.zeros((NUM_SAMPLES, NUM_CYCLES), dtype=float)
    for tube_idx, tube in enumerate(tube_names):
        fluorescence_data[tube_idx, :] = df[tube].values
    cycles = np.arange(NUM_CYCLES)

    def sigmoid(cycle, Fmax, C_half, k):
        return Fmax / (1.0 + np.exp(-k * (cycle - C_half)))

    def second_derivative(cycle, Fmax, C_half, k):
        h = 1e-2
        return (sigmoid(cycle + h, Fmax, C_half, k)
                - 2.0 * sigmoid(cycle, Fmax, C_half, k)
                + sigmoid(cycle - h, Fmax, C_half, k)) / (h * h)

    def calculate_ct(Fmax, C_half, k, num_cycles):
        max_sdm = -np.inf
        ct = 0.0
        for c in np.arange(0.0, num_cycles, 0.1):
            sdm = second_derivative(c, Fmax, C_half, k)
            if sdm > max_sdm:
                max_sdm = sdm
                ct = c
        print(f"{Fmax}, {C_half}, {k}, {num_cycles}, {ct}")
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

    fig, ax = plt.subplots(figsize=(10, 7))
    results = []
    for i in range(NUM_SAMPLES):
        fluorescence = fluorescence_data[i].copy()
        min_val = np.min(fluorescence)
        fluorescence -= min_val
        Fmax = np.max(fluorescence)
        C_half = 27.0
        k = 0.4
        Ct = calculate_ct(Fmax, C_half, k, NUM_CYCLES)
        efficiency = estimate_efficiency(fluorescence, Ct - 2, Ct + 2)
        fitted = [sigmoid(c, Fmax, C_half, k) for c in cycles]
        ax.plot(cycles, fitted, label=f'{tube_names[i]} (Ct: {Ct:.2f})')
        results.append({
            'Tube': tube_names[i],
            'Ct': Ct,
            'Efficiency': efficiency,
            'Efficiency_percent': efficiency*100
        })
    ax.set_title("qPCR Sigmoid Curves")
    ax.set_xlabel("Cycle")
    ax.set_ylabel("Fluorescence")
    ax.legend()
    st.pyplot(fig)
    st.subheader("Ct 및 효율 결과표")
    st.dataframe(pd.DataFrame(results))
else:
    st.info("qpcr_input.csv 파일을 업로드하면 분석 결과가 표시됩니다.")
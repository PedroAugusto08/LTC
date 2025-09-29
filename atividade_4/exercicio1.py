import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

sistemas = [
    {"nome": "G1(s)", "wn": 5.0,  "zeta": 0.4},
    {"nome": "G2(s)", "wn": 6.0,  "zeta": 0.5},
    {"nome": "G3(s)", "wn": 7.0,  "zeta": 1.0},
    {"nome": "G4(s)", "wn":10.0,  "zeta": 0.05},
]

# simulação
n_points = 20001

# função para achar tempo visual (2% de tolerância)
def first_persistent_time(signal, time, low, high):
    idxs = np.where((signal >= low) & (signal <= high))[0]
    if idxs.size == 0:
        return None
    for idx in idxs:
        if np.all((signal[idx:] >= low) & (signal[idx:] <= high)):
            return time[idx]
    return None

# limite visual: inferior 98,2% e teto 102%
visual_low_pct = 0.982
visual_high_pct = 1.02

resultados = []

# loop nos sistemas
for s in sistemas:
    nome = s["nome"]
    wn = float(s["wn"])
    zeta = float(s["zeta"])

    # tempo teórico
    if zeta == 0:
        ts_teo = np.nan
    else:
        ts_teo = 4.0 / (zeta * wn)

    # escolher janela de tempo baseada em ts_teo e wn
    if np.isfinite(ts_teo):
        t_final = max(6.0 * ts_teo, 8.0 / wn, 10.0)
    else:
        t_final = max(8.0 / wn, 10.0)
    t = np.linspace(0, t_final, n_points)

    # resposta ao degrau unitário
    if zeta < 1.0 - 1e-8:  # subamortecido
        wd = wn * np.sqrt(1.0 - zeta**2)
        phi = np.arccos(zeta)
        y = 1.0 - (1.0 / np.sqrt(1.0 - zeta**2)) * np.exp(-zeta * wn * t) * np.sin(wd * t + phi)
    elif abs(zeta - 1.0) <= 1e-8:  # criticamente amortecido
        y = 1.0 - np.exp(-wn * t) * (1.0 + wn * t)
    else:  # sobreamortecido
        s1 = -wn * (zeta - np.sqrt(zeta**2 - 1.0))
        s2 = -wn * (zeta + np.sqrt(zeta**2 - 1.0))
        A = s2 / (s2 - s1)
        B = -s1 / (s2 - s1)
        y = 1.0 - (A * np.exp(s1 * t) + B * np.exp(s2 * t))

    # limites visuais
    low = visual_low_pct * 1.0
    high = visual_high_pct * 1.0

    # tempo visual
    ts_vis = first_persistent_time(y, t, low, high)
    # primeiro instante que excede o limite inferior
    if ts_vis is None:
        idx = np.where(y >= low)[0]
        ts_vis = float(t[idx[0]]) if idx.size else None

    resultados.append([nome, wn, zeta, ts_teo, ts_vis])

    plt.figure(figsize=(9,5))
    plt.plot(t, y, label=f"{nome} (resposta)", linewidth=2)
    plt.axhline(1.0, color="k", linestyle="--", label="Valor final = 1.00")
    plt.axhline(low, color="orange", linestyle=":", label=f"Inferior {visual_low_pct*100:.2f}% = {low:.3f}")
    plt.axhline(high, color="orange", linestyle=":", label=f"Superior {visual_high_pct*100:.1f}% = {high:.3f}")
    if np.isfinite(ts_teo):
        plt.axvline(ts_teo, color="green", linestyle="--", label=f"T_s teórico = {ts_teo:.3f} s")
    if ts_vis is not None:
        plt.axvline(ts_vis, color="red", linestyle="--", label=f"T_s visual = {ts_vis:.3f} s")

    plt.title(f"Resposta ao degrau - {nome}")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Saída y(t)")
    plt.grid(True, ls="--", alpha=0.6)
    plt.legend()
    plt.show()

# tabela de resultados
df = pd.DataFrame(resultados, columns=["Sistema","ω_n","ζ","T_s Teórico (4/(ζ ω_n)) [s]","T_s Visual [s]"])
pd.set_option("display.float_format", lambda x: f"{x:.5f}")
print(df.to_string(index=False))

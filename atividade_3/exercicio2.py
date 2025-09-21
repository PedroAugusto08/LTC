import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# definição dos sistemas
sistemas = [
    {"nome": "G1(s)", "K": 1, "tau": 0.5},
    {"nome": "G2(s)", "K": 2, "tau": 2.0},
    {"nome": "G3(s)", "K": 5, "tau": 0.1},
]

# simulação
t_final = 15
n_points = 20001
t = np.linspace(0, t_final, n_points)

# função de resposta ao degrau
def resposta(K, tau, t):
    return K * (1 - np.exp(-t / tau))

# função para achar tempo visual (2% de tolerância)
def first_persistent_time(signal, time, final_value, tol=0.02):
    low, high = final_value * (1 - tol), final_value * (1 + tol)
    idxs = np.where((signal >= low) & (signal <= high))[0]
    if idxs.size == 0:
        return None
    for idx in idxs:
        if np.all((signal[idx:] >= low) & (signal[idx:] <= high)):
            return time[idx]
    return None

resultados = []

# loop nos sistemas
for sistema in sistemas:
    K = sistema["K"]
    tau = sistema["tau"]
    nome = sistema["nome"]

    y = resposta(K, tau, t)
    y_final = K

    # tempo teórico (4τ)
    ts_teo = 4 * tau

    # tempo visual (faixa de 2%)
    ts_vis = first_persistent_time(y, t, y_final, tol=0.018)

    resultados.append([nome, K, tau, ts_teo, ts_vis])

    plt.figure(figsize=(9, 5))
    plt.plot(t, y, label=f"{nome} (resposta)", linewidth=2)
    plt.axhline(y_final, color="k", linestyle="--", label=f"Valor final = {y_final:.2f}")
    plt.axhline(0.982 * y_final, color="orange", linestyle=":", label="98.2%")
    plt.axhline(1.02 * y_final, color="orange", linestyle=":")
    plt.axvline(ts_teo, color="green", linestyle="--", label=f"T_s teórico = {ts_teo:.2f} s")
    if ts_vis is not None:
        plt.axvline(ts_vis, color="red", linestyle="--", label=f"T_s visual = {ts_vis:.2f} s")

    plt.title(f"Resposta ao degrau - {nome}")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Saída y(t)")
    plt.grid(True, ls="--", alpha=0.7)
    plt.legend()
    plt.show()

# tabela de resultados
df = pd.DataFrame(resultados, columns=["Sistema", "K", "τ [s]", "T_s Teórico (4τ) [s]", "T_s Visual [s]"])
print(df.to_string(index=False))

import numpy as np
import matplotlib.pyplot as plt

R = 560e3
C = 10e-6
tau = R * C
V0 = 5.0

# tempos teóricos
Ts5_theo = 3 * tau  # ~16.8 s
Ts2_theo = 4 * tau  # ~22.4 s

# simulação
t_final = 40.0
n_points = 20001
t = np.linspace(0, t_final, n_points)
vc = V0 * (1 - np.exp(-t / tau))

# valores para 95% e 98.2%
p95 = 0.95 * V0
p982 = 0.982 * V0  # 98.2%

# função para encontrar o primeiro tempo em que o sinal permanece dentro de uma faixa
def first_persistent_time(signal, time, low, high):
    # índices onde sinal está dentro da faixa
    idxs = np.where((signal >= low) & (signal <= high))[0]
    if idxs.size == 0:
        return None
    # testar cada candidato
    for idx in idxs:
        if np.all((signal[idx:] >= low) & (signal[idx:] <= high)):
            return time[idx]
    return None

# encontrar tempos "práticos" usando np.where + persistência
t95_sim = first_persistent_time(vc, t, p95, V0 * 1.05)   # faixa 95%
t982_sim = first_persistent_time(vc, t, p982, V0 * 1.02)  # faixa 98.2%

# fallbacks (caso a persistência não seja satisfeita)
if t95_sim is None:
    idx = np.where(vc >= p95)[0]
    t95_sim = t[idx[0]] if idx.size else None
if t982_sim is None:
    idx = np.where(vc >= p982)[0]
    t982_sim = t[idx[0]] if idx.size else None

print("Constante de tempo: tau = {:.4f} s".format(tau))
print("Tempos teóricos:")
print("T_s(5%) ≈ 3·tau = {:.4f} s".format(Ts5_theo))
print("T_s(2%) ≈ 4·tau = {:.4f} s".format(Ts2_theo))
print()
print("Tempos obtidos na simulação (por np.where e persistência):")
print("Tempo em que vc alcança/permanece em 95%: {:.4f} s".format(t95_sim))
print("Tempo em que vc alcança/permenece em 98.2%: {:.4f} s".format(t982_sim))
print()
# diferenças relativas (em %)
if t95_sim is not None:
    err95 = 100*(t95_sim - Ts5_theo)/Ts5_theo
    print("  Diferença entre simulado 95% e T_s(5%) (3·tau): {:.3f}%".format(err95))
if t982_sim is not None:
    err982 = 100*(t982_sim - Ts2_theo)/Ts2_theo
    print("  Diferença entre simulado 98.2% e T_s(2%) (4·tau): {:.3f}%".format(err982))

# ---------------------------
# Plot 1: Teórico (3τ e 4τ)
# ---------------------------
plt.figure(figsize=(10,6))
plt.plot(t, vc, label=r'$v_C(t)$ (simulação)', linewidth=2)
plt.axhline(V0, linestyle='--', linewidth=1, label='Valor final ({} V)'.format(V0))
plt.axvline(Ts5_theo, color='orange', linestyle='--', label=r'$3\tau$ = {:.2f} s'.format(Ts5_theo))
plt.axvline(Ts2_theo, color='green', linestyle='--', label=r'$4\tau$ = {:.2f} s'.format(Ts2_theo))
plt.title('Teórico (3τ e 4τ)')
plt.xlabel('Tempo [s]')
plt.ylabel('v_C(t) [V]')
plt.grid(True, which='both', ls='--')
plt.legend()
plt.show()

# ---------------------------
# Plot 2: Prático (95% e 98.2%)
# ---------------------------
plt.figure(figsize=(10,6))
plt.plot(t, vc, label=r'$v_C(t)$ (simulação)', linewidth=2)
plt.axhline(p95, color='orange', linestyle=':', label='95% = {:.2f} V'.format(p95))
plt.axhline(p982, color='green', linestyle=':', label='98.2% = {:.2f} V'.format(p982))
plt.axhline(V0, color='k', linestyle='--', label='Valor final ({} V)'.format(V0))

if t95_sim is not None:
    plt.axvline(t95_sim, color='orange', linestyle='--', label='t95 (sim) = {:.2f} s'.format(t95_sim))
if t982_sim is not None:
    plt.axvline(t982_sim, color='green', linestyle='--', label='t98.2 (sim) = {:.2f} s'.format(t982_sim))

plt.title('Prático (95% e 98.2%)')
plt.xlabel('Tempo [s]')
plt.ylabel('v_C(t) [V]')
plt.grid(True, which='both', ls='--')
plt.legend()
plt.show()

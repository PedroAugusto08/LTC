import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

L = 10e-3
C = 10e-6

# resistência crítica
R_cr = 2.0 * np.sqrt(L / C)

R_sub = 50.0
R_crit = R_cr
R_over = 120.0

Rs = [R_sub, R_crit, R_over]
labels = ['subamortecido (R=50 Ω)', f'criticamente amortecido (R={R_cr:.4f} Ω)', f'superamortecido (R={R_over:.1f} Ω)']
styles = ['-', '--', '-.']

# tempo baseado na frequência natural
omega0 = 1.0 / np.sqrt(L * C)
T0 = 2 * np.pi / omega0
t_end = max(5 * T0, 0.02)
t = np.linspace(0.0, t_end, 2000)

plt.figure(figsize=(8,4.5))

for R, lab, st in zip(Rs, labels, styles):
    num = [1.0]
    den = [L * C, R * C, 1.0]
    G = ctrl.TransferFunction(num, den)
    t_out, y = ctrl.step_response(G, T=t)
    # calcular zeta para informação
    zeta = (R / 2.0) * np.sqrt(C / L)
    print(f"R = {R:.6f} Ω  |  ζ = {zeta:.6f}")
    plt.plot(t_out, y, st, label=lab, linewidth=1.6)

plt.xlabel('Tempo [s]')
plt.ylabel('v_C(t) [V] (entrada degrau unitário)')
plt.title('Comparação: respostas ao degrau — sub / crítico / superamortecido')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('comparacao_rlc_respostas.png', dpi=300, bbox_inches='tight')
plt.show()
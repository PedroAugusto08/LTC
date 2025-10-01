import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Definição do sistema G(s) = 1 / (s^2 + 1.2 s + 9)
num = [1.0]
den = [1.0, 1.2, 9.0]
G = ctrl.tf(num, den)

# parâmetros do sistema de segunda ordem (a partir dos coeficientes)
a1 = den[1]   # 1.2
a0 = den[2]   # 9.0
omega_n = np.sqrt(a0)
zeta = a1 / (2 * omega_n)

# polos
polos = ctrl.poles(G)

# vetor de tempo (ajuste se quiser intervalo maior/menor)
t = np.linspace(0, 10, 1000)

# resposta ao degrau em malha aberta (entrada unitária)
t_out, y = ctrl.step_response(G, T=t)

# valor teórico em regime (valor DC = G(0) = lim_{s->0} G(s))
y_ss_teo = float(ctrl.evalfr(G, 0).real)  # deve ser 1/9 ≈ 0.111111...

# valor numérico no tempo final (aproximação de y_ss)
y_ss_num = y[-1]

# saída de resumo
print("Sistema de segunda ordem (malha aberta): G(s) = 1/(s^2 + 1.2 s + 9)")
print(f"Polos: {polos}")
print(f"Frequência natural ω_n = {omega_n:.4f} rad/s")
print(f"Razão de amortecimento ζ = {zeta:.4f}")
print(f"\nValor em regime (teórico) y_ss = G(0) = {y_ss_teo:.6f}")
print(f"Valor em regime (numérico, t_final={t_out[-1]:.1f}s) y(t_final) = {y_ss_num:.6f}")

# Plot
plt.figure(figsize=(9, 5))
plt.plot(t_out, y, label='Resposta (malha aberta)')
plt.axhline(y=y_ss_teo, linestyle='--', linewidth=1, color='orange',
            label=f'y_ss (teórico) = {y_ss_teo:.6f}')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída y(t)')
plt.title('Resposta ao degrau unitário — malha aberta: G(s)=1/(s^2+1.2s+9)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('saida_segunda_malha_aberta.png', dpi=200)
plt.show()

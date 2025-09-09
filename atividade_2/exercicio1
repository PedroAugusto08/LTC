import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

a_list = [0.01, 0.02, 0.05, 0.1, 0.5, 1.0, 2.0]

# --- figura 1: polos ---
plt.figure(figsize=(6.5,5))
for a in a_list:
    num = [1.0]
    den = [1.0, a, 0.0] # s^2 + a s + 0
    G = ctrl.TransferFunction(num, den)
    poles = ctrl.poles(G)
    plt.plot(poles.real, poles.imag, 'o', label=f'a={a}')
    print(f"a = {a:>4}  -> polos: {', '.join([f'{p:.6g}' for p in poles])}")
plt.axhline(0, color='k', linewidth=0.6)
plt.axvline(0, color='k', linewidth=0.6)
plt.xlabel('Re(s)')
plt.ylabel('Im(s)')
plt.title('Polos de G(s)=1/[s(s+a)]')
plt.grid(True, which='both', ls='--', alpha=0.6)
plt.legend(loc='best', fontsize='small')
plt.tight_layout()
plt.savefig('polos_abertos_a.png', dpi=300, bbox_inches='tight')

# --- figura 2: respostas ao degrau ---
plt.figure(figsize=(8,5))

t_end = 2.0
t = np.linspace(0.0, t_end, 2000)

for a in a_list:
    num = [1.0]
    den = [1.0, a, 0.0]
    G = ctrl.TransferFunction(num, den)
    t_out, y = ctrl.step_response(G, T=t)

    idx1, idx0 = -1, -11
    slope_est = (y[idx1] - y[idx0]) / (t_out[idx1] - t_out[idx0])

    print(f"a = {a:>4}  -> slope_est ≈ {slope_est:.6g}  (unidade: V/s para entrada degrau unitário)")

    plt.plot(t_out, y, label=f'a={a}')

plt.xlabel('Tempo [s]')
plt.ylabel('Resposta ao degrau y(t) [unidade do sistema]')
plt.title('Respostas ao degrau de G(s)=1/[s(s+a)] para diferentes valores de a')
plt.grid(True)
plt.legend(fontsize='small', ncol=2)
plt.tight_layout()
plt.savefig('respostas_degrau_a.png', dpi=300, bbox_inches='tight')
plt.show()
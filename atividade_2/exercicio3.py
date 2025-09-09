import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

a_list = [0.01, 0.02, 0.05, 0.1, 0.5, 1.0, 2.0]

# ---- FIGURA 1: polos da malha fechada ----
plt.figure(figsize=(7,6))
for a in a_list:
    # malha fechada T(s) = 1 / (s^2 + a s + 1)
    num = [1.0]
    den = [1.0, a, 1.0]
    T = ctrl.TransferFunction(num, den)

    poles = ctrl.poles(T)
    zeta = a / 2.0

    disc = a*a - 4.0
    if disc < 0:
        cls = "subamortecido (polos complexos)"
    elif np.isclose(disc, 0.0):
        cls = "critic. amortecido (polos reais iguais)"
    else:
        cls = "superamortecido (polos reais distintos)"

    print(f"a = {a:>4} | zeta = {zeta:.6g} | {cls} | polos: {', '.join([f'{p:.6g}' for p in poles])}")

    plt.plot(poles.real, poles.imag, 'o', label=f'a={a}')

plt.axhline(0, color='k', linewidth=0.6)
plt.axvline(0, color='k', linewidth=0.6)
plt.xlabel('Re(s)')
plt.ylabel('Im(s)')
plt.title('Polos da malha fechada T(s)=1/(s^2 + a s + 1)')
plt.grid(True, which='both', ls='--', alpha=0.6)
plt.legend(loc='best', fontsize='small')
plt.tight_layout()
plt.savefig('polos_malha_fechada.png', dpi=300, bbox_inches='tight')

# ---- FIGURA 2: respostas ao degrau ----
plt.figure(figsize=(8,5))

t_end = 50.0
t = np.linspace(0.0, t_end, 3000)

for a in a_list:
    num = [1.0]
    den = [1.0, a, 1.0]
    T = ctrl.TransferFunction(num, den)
    t_out, y = ctrl.step_response(T, T=t)

    plt.plot(t_out, y, label=f'a={a}')

plt.xlabel('Tempo [s]')
plt.ylabel('Resposta ao degrau y(t)')
plt.title('Respostas ao degrau de T(s)=1/(s^2 + a s + 1)')
plt.grid(True)
plt.legend(fontsize='small', ncol=2)
plt.tight_layout()
plt.savefig('respostas_malha_fechada.png', dpi=300, bbox_inches='tight')
plt.show()

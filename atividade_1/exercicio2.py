import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

R = 50.0
L = 10e-3
C = 10e-6

num = [1.0]
den = [L * C, R * C, 1.0]

G = ctrl.TransferFunction(num, den)

print("Sistema G(s):")
print(G)

omega0 = 1.0 / np.sqrt(L * C)
zeta = (R / 2.0) * np.sqrt(C / L)
T0 = 2 * np.pi / omega0

print(f"\nω0 = {omega0:.2f} rad/s")
print(f"ζ  = {zeta:.4f}")
print(f"Período natural T0 ≈ {T0*1e3:.3f} ms")

t_end = max(5 * T0, 0.02)
t = np.linspace(0.0, t_end, 2000)

t_out, vC = ctrl.step_response(G, T=t)

steady_state = vC[-1]
print(f"Valor em regime permanente aproximado: vC(∞) ≈ {steady_state:.6f} V")

dvC_dt = np.gradient(vC, t_out)
i_t = C * dvC_dt

plt.subplot(2,1,1)
plt.plot(t_out, vC, linewidth=1.6, label='$v_C(t)$')
plt.ylabel('Tensão $v_C(t)$ [V]')
plt.title('Resposta ao Degrau Unitário — $V_C(s)/V_{in}(s)$')
plt.grid(True)
plt.legend(loc='best')

plt.show()
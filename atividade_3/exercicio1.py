import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

R = 50.0
C = 10e-6

num = [1.0]
den = [R * C, 1.0]

G = ctrl.TransferFunction(num, den)

print("Sistema G(s):")
print(G)

t = np.linspace(0.0, 0.02, 2000)

t_out, vC = ctrl.step_response(G, T=t)

steady_state = vC[-1]
print(f"Valor em regime permanente aproximado: vC(∞) ≈ {steady_state:.6f} V")

dvC_dt = np.gradient(vC, t_out)
i_t = C * dvC_dt

plt.plot(t_out, vC, linewidth=1.6, label='$v_C(t)$')
plt.ylabel('Tensão $v_C(t)$ [V]')
plt.title('Resposta ao Degrau Unitário — $V_C(s)/V_{in}(s)$')
plt.grid(True)
plt.legend(loc='best')

plt.show()
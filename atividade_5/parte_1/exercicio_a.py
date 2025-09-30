import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# G(s) = 1/(3 s)
G = ctrl.tf([1], [3, 0])

t = np.linspace(0, 30, 1000)

# resposta ao degrau unitário
t_out, y_num = ctrl.step_response(G, T=t)

# y(t) = t/3
y_analytic = t_out / 3.0

plt.figure(figsize=(9, 5))
plt.plot(t_out, y_num, label='Resposta (control.step_response)')
plt.plot(t_out, y_analytic, '--', label=r'Resposta analítica $y(t)=t/3$')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída $y(t)$')
plt.title('Resposta ao degrau unitário — malha aberta: $G(s)=1/(3s)$')
plt.grid(True)
plt.legend()
plt.xlim(0, 30)
plt.tight_layout()
plt.show()

# Informação numérica resumida
print(f"t final = {t_out[-1]:.1f} s")
print(f"y(t_final) (numérico)  = {y_num[-1]:.6f}")
print(f"y(t_final) (analítico) = {y_analytic[-1]:.6f}")

# Observação sobre erro estacionário (útil para o relatório)
e_t = 1 - y_analytic  # erro entre referência unitária e saída analítica
print("\nObservação:")
print("- A saída cresce linearmente (rampa) com inclinação 1/3: y(t)=t/3.")
print("- Em malha aberta, para entrada degrau unitário, y(t) -> infinito quando t -> infinito;")
print("  portanto o 'erro em regime estacionário' no sentido usual (lim t->inf e(t)) não é finito/definido.")

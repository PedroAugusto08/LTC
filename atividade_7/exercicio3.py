import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

# numerador e denominador
num = [1] # 1
den = [1, 6, 5, 0]   # s^3 + 6 s^2 + 5 s

G = ctrl.TransferFunction(num, den)

# valores Ziegler-Nichols para PI
Kcr = 30.00
Pcr = 2.81
Kp = 0.45 * Kcr   # = 13.5
Ti = Pcr / 1.2   # ≈ 2.342
Ki = Kp / Ti   # ≈ 5.763

print(f"Kp = {Kp:.4f}")
print(f"Ti = {Ti:.4f} s")
print(f"Ki = {Ki:.4f}")

# controlador PI: C(s) = Kp + Ki/s -> (Kp*s + Ki)/s
C_PI = ctrl.TransferFunction([Kp, Ki], [1, 0])

# malha fechada com PI
Gcl_PI = ctrl.feedback(C_PI * G, 1)

# malha fechada com ganho crítico
Gcl_Kcr = ctrl.feedback(Kcr * G, 1)

# resposta ao degrau
t = np.linspace(0, 40, 5000)
t_PI, y_PI = ctrl.step_response(Gcl_PI, T=t)
t_Kcr, y_Kcr = ctrl.step_response(Gcl_Kcr, T=t)

# gráfico 1 (PI)
plt.figure(figsize=(10,4))
plt.plot(t_PI, y_PI, label='Controlador PI (Ziegler-Nichols)')
plt.title('Resposta ao Degrau com Controlador PI (Ziegler-Nichols)')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída')
plt.grid(True)
plt.legend()
plt.show()

# gráfico 2 (comparação)
plt.figure(figsize=(10,4))
plt.plot(t_PI, y_PI, label='Controlador PI (Ziegler-Nichols)')
plt.plot(t_Kcr, y_Kcr, label='Controlador Proporcional com Kcr = 30', linestyle='--')
plt.title('Comparação: PI vs Proporcional com Kcr')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída')
plt.grid(True)
plt.legend()
plt.show()

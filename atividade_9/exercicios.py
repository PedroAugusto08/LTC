import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# ----- G1(s) = 1000 / ((s+10)(s+100)) -----
num = [1000]
den = [1, 110, 1000]
G = ctrl.TransferFunction(num, den)
print("Função de transferência G1(s):")
print(G)
ctrl.bode(G, dB=True, Hz=False, omega_limits=[0.1, 1000])
plt.show()

# ----- G2(s) = (s + 100) / ((s + 2)(s + 25)) -----
num2 = [1, 100]
den2 = [1, 27, 50]
G2 = ctrl.TransferFunction(num2, den2)
print("\nFunção de transferência G2(s):")
print(G2)
ctrl.bode(G2, dB=True, Hz=False, omega_limits=[0.1, 1000])
plt.show()

# ----- G3(s) = 100 / (s^2 + 2 s + 50) -----
num3 = [100]
den3 = [1, 2, 50]
G3 = ctrl.TransferFunction(num3, den3)
print("\nFunção de transferência G3(s):")
print(G3)
ctrl.bode(G3, dB=True, Hz=False, omega_limits=[0.1, 1000])
plt.show()

# ----- G4(s) = (s - 6) / ((s + 3)(s^2 + 12 s + 50)) -----
num4 = [1, -6]
den4 = [1, 15, 86, 150]
G4 = ctrl.TransferFunction(num4, den4)
print("\nFunção de transferência G4(s):")
print(G4)
ctrl.bode(G4, dB=True, Hz=False, omega_limits=[0.1, 1000])
plt.show()

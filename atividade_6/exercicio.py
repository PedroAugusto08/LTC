import control as ctrl
import matplotlib.pyplot as plt

# sistema 1
num = [1, 10]  # s + 10
den = [1, 7, 10, 0]  # s^3 + 7 s^2 + 10 s

# sistema 2
num2 = [1, 3]  # s + 3
den2 = [1, 7, 10, 0]  # s^3 + 7 s^2 + 10 s

# sistema 3
num3 = [1]  # 1
den3 = [1, 5, 9, 5, 0] # s^4 + 5 s^3 + 9 s^2 + 5 s

num4 = [1, 3] # s + 3
den4 = [1, 5, 20, 16, 0] # s^4 + 5 s^3 + 20 s^2 + 16 s

num5 = [1, 2, 4] # s^2 + 2 s + 4
den5 = [1, 11.4, 39, 43.6, 24, 0] # s^5 + 11.4 s^4 + 39 s^3 + 43.6 s^2 + 24 s

# funções de transferência
G1 = ctrl.TransferFunction(num, den)
G2 = ctrl.TransferFunction(num2, den2)
G3 = ctrl.TransferFunction(num3, den3)
G4 = ctrl.TransferFunction(num4, den4)
G5 = ctrl.TransferFunction(num5, den5)

# plot sistema 1
print("Funcao de transferencia G1(s):")
print(G1)
ctrl.rlocus(G1)
plt.grid(True)
plt.title("Lugar das Raizes - Sistema 1")
plt.show()

# plot sistema 2
print("Funcao de transferencia G2(s):")
print(G2)
ctrl.rlocus(G2)
plt.grid(True)
plt.title("Lugar das Raizes - Sistema 2")
plt.show()

# plot sistema 3
print("Funcao de transferencia G3(s):")
print(G3)
ctrl.rlocus(G3)
plt.grid(True)
plt.title("Lugar das Raizes - Sistema 3")
plt.show()

# plot sistema 4
print("Funcao de transferencia G4(s):")
print(G4)
ctrl.rlocus(G4)
plt.grid(True)
plt.title("Lugar das Raizes - Sistema 4")
plt.show()

# plot sistema 5
print("Funcao de transferencia G5(s):")
print(G5)
ctrl.rlocus(G5)
plt.grid(True)
plt.title("Lugar das Raizes - Sistema 5")
plt.show()

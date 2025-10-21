import control as ctrl
import matplotlib.pyplot as plt

# numerador e denominador
num = [1] # 1
den = [1 , 6 , 5 , 0] # s^3 + 6 s^2 + 5 s

# função de transferência
G = ctrl.TransferFunction(num, den)
print("Função de transferência G(s):")
print(G)

# plot
print("Funcao de transferencia G(s):")
print(G)
ctrl.rlocus(G)
plt.grid(True)
plt.title("Lugar das Raizes - Sistema 1")
plt.show()

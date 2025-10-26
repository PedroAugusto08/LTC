import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

# numerador e denominador
num = [1] # 1
den = [1, 6, 5, 0]   # s^3 + 6 s^2 + 5 s

# função de transferência em loop aberto
G = ctrl.TransferFunction(num, den)
print("Função de transferência G(s):")
print(G)

# ganho crítico
Kcr = 30

# função de transferência
Gcl = ctrl.feedback(Kcr * G, 1)

# simulação da resposta ao degrau
t_final = 60.0
t = np.linspace(0, t_final, 5000)
t_out, y_out = ctrl.step_response(Gcl, T=t)

# plot da resposta ao degrau
plt.figure(figsize=(10,4))
plt.plot(t_out, y_out, label='Resposta')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída')
plt.title('Resposta ao degrau em malha fechada com K = 30')
plt.grid(True)


# detectar picos e calcular tempo entre os dois primeiros
peaks_idx = []
for i in range(1, len(y_out) - 1):
	if y_out[i - 1] < y_out[i] and y_out[i] > y_out[i + 1]:
		peaks_idx.append(i)

print ("\n")

if len(peaks_idx) >= 2:
	i1, i2 = peaks_idx[0], peaks_idx[1]
	t1, y1 = t_out[i1], y_out[i1]
	t2, y2 = t_out[i2], y_out[i2]
	dt12 = t2 - t1
	print(f"Pcr (entre 1º e 2º picos) = {dt12:.6f} s")

	# marcar os dois primeiros picos
	plt.plot([t1], [y1], 'o', color='red', label='1º pico')
	plt.plot([t2], [y2], 'o', color='purple', label='2º pico')

	# traçado horizontal entre os picos indicando Δt
	y_span = (np.max(y_out) - np.min(y_out))
	y_line = max(y1, y2) + 0.02 * y_span
	ymin, ymax = plt.ylim()
	if y_line > ymax:
		plt.ylim(ymin, y_line + 0.05 * (ymax - ymin if ymax > ymin else 1.0))
	plt.annotate('', xy=(t2, y_line), xytext=(t1, y_line),
				 arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5))
	plt.text((t1 + t2) / 2.0, y_line, f" Δt = {dt12:.3f} s", color='gray',
			 ha='center', va='bottom')

plt.legend()
plt.show()

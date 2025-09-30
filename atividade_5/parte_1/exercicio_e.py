import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# G(s) = 1/(3 s)
G = ctrl.tf([1], [3, 0])

t = np.linspace(0, 30, 1000)

# ganhos a serem testados (mesmos do item c)
Ks = [1, 10]

resultados = []

for K in Ks:
	# ganho no ramo direto
	Gd = ctrl.series(ctrl.tf([K], [1]), G)
	T_closed = ctrl.feedback(Gd, 1)
 
	polos = ctrl.poles(T_closed)

	# resposta ao degrau unitário
	t_out, y = ctrl.step_response(T_closed, T=t)

	# valor teórico de regime estacionário
	y_ss_teo = 1.0
 
	# valor numérico aproximado (t_final)
	y_final_num = y[-1]
 
	# constante de tempo estimada (aprox quando y alcança 63.2% do valor final)
	y_tau = 0.632 * y_ss_teo
	# encontrar primeiro índice onde y >= y_tau
	idx_tau = np.argmax(y >= y_tau)
	tau_est = t_out[idx_tau] if idx_tau > 0 else np.nan

	resultados.append({
		'K': K,
		'polos': polos,
		'y_final_num': y_final_num,
		'y_ss_teo': y_ss_teo,
		'tau_est': tau_est,
		'tau_teo': 3.0 / K
	})

	print(f"\n=== Ganho no ramo direto: K = {K} ===")
	print(f"Polos: {polos}")
	print(f"y(t_final) (numérico) = {y_final_num:.6f}")
	print(f"y_ss (teórico)        = {y_ss_teo:.6f}")
	print(f"Constante de tempo teórica tau = {3.0/K:.4f} s")
	print(f"Constante de tempo estimada     = {tau_est:.4f} s")

	plt.figure(figsize=(8, 4.8))
	plt.plot(t_out, y, label=f"y(t) — K direto={K}")
	plt.axhline(y=y_ss_teo, linestyle='--', color='orange', linewidth=1, label=f"y_ss= {y_ss_teo:.2f}")
	plt.xlabel("Tempo (s)")
	plt.ylabel("Saída y(t)")
	plt.title(f"Resposta ao degrau — ganho direto K={K}")
	plt.grid(True)
	plt.legend()
	plt.tight_layout()
	fname = f"saida_direto_K{K}.png"
	plt.savefig(fname, dpi=200)
	plt.close()
	print(f"Gravado: {fname}")

# figura comparativa
plt.figure(figsize=(8, 4.8))
for r in resultados:
	K = r['K']
	Gd = ctrl.series(ctrl.tf([K], [1]), G)
	T_closed = ctrl.feedback(Gd, 1)
	t_out, y = ctrl.step_response(T_closed, T=t)
	plt.plot(t_out, y, label=f"K={K}")

plt.axhline(1.0, linestyle='--', color='black', linewidth=1, label='y_ss = 1')
plt.xlabel("Tempo (s)")
plt.ylabel("Saída y(t)")
plt.title("Comparação respostas — ganho no ramo direto")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("comparacao_respostas_ganho_direto.png", dpi=200)
plt.close()
print("Gravado: comparacao_respostas_ganho_direto.png")

# resumo final
print("\nResumo:")
for r in resultados:
	print(f"K={r['K']}: polo={r['polos'][0]:.4f}, tau_teo={r['tau_teo']:.4f}s, tau_est={r['tau_est']:.4f}s, y_final={r['y_final_num']:.3f}")
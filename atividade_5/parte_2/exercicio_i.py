import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

"""
Exercício (i): Considere agora os MESMOS ganhos do item (g), porém aplicados NO RAMO DIRETO.

Item (g): Estrutura considerada foi G(s) em série e ganho K na realimentação (feedback):
	T_g(s) = G(s) / (1 + K G(s))

Agora (i): Ganho K em série com a planta antes do somador (feedback unitário):
	L(s) = K * G(s)
	T_i(s) = K G(s) / (1 + K G(s))

Planta original:
	G(s) = 1 / (s^2 + 1.2 s + 9)

Então:
	T_i(s) = K / (s^2 + 1.2 s + 9 + K)

Forma padrão 2ª ordem: ω_n^2 = 9 + K ; 2 ζ ω_n = 1.2
	ω_n = sqrt(9 + K)
	ζ = 1.2 / (2 ω_n)

Ganho DC (r -> degrau unitário):
	y_ss = K / (9 + K)

Comparação importante:
  Caso (g) (ganho no feedback): y_ss_g = 1 / (9 + K)
  Caso (i) (ganho direto):      y_ss_i = K / (9 + K)
  Soma: y_ss_g + y_ss_i = (1 + K)/(9 + K) ≠ 1 (apenas observação, sem relação direta).
  Note que quanto maior K, mais o sistema com ganho direto aproxima y_ss_i -> 1.
  Já no caso (g), y_ss_g diminui para 0 conforme K cresce.
"""

# Planta
G = ctrl.tf([1.0], [1.0, 1.2, 9.0])

t = np.linspace(0, 10, 1000)
Ks = [1, 10]

resultados = []

for K in Ks:
	# ganho no ramo direto: série K * G(s)
	Gd = ctrl.series(ctrl.tf([K], [1]), G)  # K*G(s)
	T_closed = ctrl.feedback(Gd, 1)         # K G /(1 + K G)

	# resposta degrau
	t_out, y = ctrl.step_response(T_closed, T=t)

	# polos, parâmetros teóricos
	polos = ctrl.poles(T_closed)
	wn = np.sqrt(9.0 + K)
	zeta = 1.2 / (2.0 * wn)
	y_ss_teo = K / (9.0 + K)
	y_ss_num = float(y[-1])
	e_ss_num = 1.0 - y_ss_num

	print(f"\n=== K = {K} (ganho no ramo direto) ===")
	print(f"Polos: {polos}")
	print(f"ω_n (teórico) = {wn:.4f} rad/s")
	print(f"ζ (teórico)   = {zeta:.4f}")
	print(f"y_ss (teórico) = {y_ss_teo:.6f}")
	print(f"y_ss (numérico) = {y_ss_num:.6f}")
	print(f"Erro estacionário e_ss ≈ {e_ss_num:.6f}")

	plt.figure(figsize=(8, 4.8))
	plt.plot(t_out, y, label=f"Saída y(t), K={K}")
	plt.axhline(y=y_ss_teo, linestyle='--', color='orange',
				label=f"y_ss teórico = {y_ss_teo:.3f}")
	plt.xlabel("Tempo (s)")
	plt.ylabel("Saída y(t)")
	plt.title(f"Resposta ao degrau — ganho DIRETO K={K}")
	plt.grid(True)
	plt.legend()
	plt.tight_layout()
	fname = f"saida_direto2_K{K}.png"
	plt.savefig(fname, dpi=200)
	plt.close()
	print(f"Gravado: {fname}")

	resultados.append({
		'K': K,
		'polos': polos,
		'wn': wn,
		'zeta': zeta,
		'y_ss_teo': y_ss_teo,
		'y_ss_num': y_ss_num,
		'e_ss_num': e_ss_num
	})

# Figura comparativa das respostas (ganho direto)
plt.figure(figsize=(8, 4.8))
for r in resultados:
	K = r['K']
	Gd = ctrl.series(ctrl.tf([K], [1]), G)
	T_closed = ctrl.feedback(Gd, 1)
	t_out, y = ctrl.step_response(T_closed, T=t)
	plt.plot(t_out, y, label=f"K={K} (y_ss={r['y_ss_teo']:.2f})")

plt.xlabel("Tempo (s)")
plt.ylabel("Saída y(t)")
plt.title("Comparação respostas — ganho direto (exercício i)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("comparacao_respostas_ganho_direto.png", dpi=200)
plt.close()
print("Gravado: comparacao_respostas_ganho_direto.png")

# (Opcional) Comparação direta com caso (g) para o mesmo K
for K in Ks:
	# Caso (g): ganho na realimentação => T_g = G/(1 + K G)
	K_tf = ctrl.tf([K], [1])
	T_g = ctrl.feedback(G, K_tf)
	# Caso (i): ganho direto => T_i = K G /(1 + K G)
	T_i = ctrl.feedback(K * G, 1)
	t_out, y_g = ctrl.step_response(T_g, T=t)
	_, y_i = ctrl.step_response(T_i, T=t)

	plt.figure(figsize=(8, 4.8))
	plt.plot(t_out, y_g, label=f"Caso (g) y_g (y_ss={1/(9+K):.2f})")
	plt.plot(t_out, y_i, label=f"Caso (i) y_i (y_ss={K/(9+K):.2f})")
	plt.xlabel("Tempo (s)")
	plt.ylabel("Saída y(t)")
	plt.title(f"Comparação casos (g) vs (i) — K={K}")
	plt.grid(True)
	plt.legend()
	plt.tight_layout()
	fname = f"comparacao_g_vs_i_K{K}.png"
	plt.savefig(fname, dpi=200)
	plt.close()
	print(f"Gravado: {fname}")

print("\nResumo final:")
for r in resultados:
	print(f"K={r['K']}: polos={r['polos']}, wn={r['wn']:.3f}, zeta={r['zeta']:.3f}, y_ss={r['y_ss_num']:.3f}, e_ss={r['e_ss_num']:.3f}")

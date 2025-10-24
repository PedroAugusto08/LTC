import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# numerador e denominador
num = [1]
den = [1, 6, 5, 0]
G = ctrl.TransferFunction(num, den)

# simulação
n_points = 2000
t_final = 20.0
t = np.linspace(0, t_final, n_points)

# função para achar tempo visual (2% de tolerância)
def first_persistent_time(signal, time, low, high):
	idxs = np.where((signal >= low) & (signal <= high))[0]
	if idxs.size == 0:
		return None
	for idx in idxs:
		if np.all((signal[idx:] >= low) & (signal[idx:] <= high)):
			return time[idx]
	return None

# limites visuais: inferior 98,2% e teto 102%
visual_low_pct = 0.982
visual_high_pct = 1.02
low = visual_low_pct * 1.0
high = visual_high_pct * 1.0

# parâmetros críticos
Kcr = 30.00
Pcr = 2.81

# controlador PID por Ziegler–Nichols
Kp0 = 0.6 * Kcr
Ti0 = 0.5 * Pcr
Td0 = 0.125 * Pcr
Ki0 = Kp0 / Ti0
Kd0 = Kp0 * Td0

print("\nInicial:")
print(f"Kp0={Kp0:.6f}, Ki0={Ki0:.6f}, Kd0={Kd0:.6f}")

# avalia métricas (Ts visual e overshoot) para um PID
def evaluate_pid(Kp, Ki, Kd):
	"""Retorna Ts, Mp, y_inf, t, y para o PID dado; ignora candidatos inválidos."""
	# C(s) = (Kd s^2 + Kp s + Ki) / s
	Cpid = ctrl.TransferFunction([Kd, Kp, Ki], [1, 0])
	Gcl = ctrl.feedback(Cpid * G, 1)
	try:
		tr, yr = ctrl.step_response(Gcl, T=t)
	except Exception:
		return None
	if np.any(~np.isfinite(yr)):
		return None
	y_inf = float(yr[-1])
	Mp = (np.max(yr) - 1.0) * 100.0
	Ts = first_persistent_time(yr, tr, low, high)
	if Ts is None:
		idx = np.where(yr >= low)[0]
		Ts = float(tr[idx[0]]) if idx.size else np.inf
	return {
		"Kp": Kp, "Ki": Ki, "Kd": Kd,
		"t": tr, "y": yr, "y_inf": y_inf,
		"Mp": float(Mp), "Ts": float(Ts)
	}

# critérios de projeto
TS_MAX = 7.0
MP_MAX = 20.0

# busca ao redor do ZN (multiplicadores)
mults_coarse = [0.5, 0.75, 1.0, 1.25, 1.5]
tested = 0
best_feasible = None  # melhor que satisfaz os critérios
best_near = None      # melhor (menor custo) mesmo que não satisfaça

def cost(candidate):
	pen_ts = max(0.0, candidate["Ts"] - TS_MAX) / TS_MAX
	pen_mp = max(0.0, candidate["Mp"] - MP_MAX) / MP_MAX
	return 10.0 * (pen_ts + pen_mp) + candidate["Ts"]

for mP in mults_coarse:
	for mI in mults_coarse:
		for mD in mults_coarse:
			cand = evaluate_pid(Kp0 * mP, Ki0 * mI, Kd0 * mD)
			if cand is None:
				continue
			tested += 1
			ok = (cand["Ts"] < TS_MAX) and (cand["Mp"] < MP_MAX)
			if ok:
				if (best_feasible is None) or (cand["Ts"] < best_feasible["Ts"]):
					best_feasible = cand
			else:
				if (best_near is None) or (cost(cand) < cost(best_near)):
					best_near = cand

# refino local ao redor do melhor candidato
def refine_around(base, scales=(0.8, 0.9, 1.0, 1.1, 1.2)):
	global tested
	best_ok = base if ((base is not None) and (base["Ts"] < TS_MAX) and (base["Mp"] < MP_MAX)) else None
	best_alt = base
	if base is None:
		return None, None
	for mP in scales:
		for mI in scales:
			for mD in scales:
				cand = evaluate_pid(base["Kp"] * mP, base["Ki"] * mI, base["Kd"] * mD)
				if cand is None:
					continue
				tested += 1
				ok = (cand["Ts"] < TS_MAX) and (cand["Mp"] < MP_MAX)
				if ok:
					if (best_ok is None) or (cand["Ts"] < best_ok["Ts"]):
						best_ok = cand
				else:
					if (best_alt is None) or (cost(cand) < cost(best_alt)):
						best_alt = cand
	return best_ok, best_alt

if best_feasible is None:
	ref_ok, ref_alt = refine_around(best_near)
	best_feasible = ref_ok
	best_near = ref_alt
else:
	ref_ok, ref_alt = refine_around(best_feasible)
	best_feasible = ref_ok or best_feasible
	best_near = ref_alt or best_near

print(f"\nCombinações avaliadas: {tested}")

chosen = best_feasible or best_near
if chosen is None:
	raise RuntimeError("Nenhum candidato válido foi avaliado. Verifique a instalação da biblioteca 'control'.")

meets = (chosen["Ts"] < TS_MAX) and (chosen["Mp"] < MP_MAX)

print("\nResultado final:")
print(f"Atende critérios? {'SIM' if meets else 'NÃO'}  (Ts={chosen['Ts']:.3f}s, Mp={chosen['Mp']:.2f}%)")
print(f"Ganhos: Kp={chosen['Kp']:.6f}, Ki={chosen['Ki']:.6f}, Kd={chosen['Kd']:.6f}")

# gráfico (PID ajustado)
tr, yr = chosen["t"], chosen["y"]
Mp = chosen["Mp"]
Ts = chosen["Ts"]

plt.figure(figsize=(9,5))
plt.plot(tr, yr, label="G(s) com PID (ajustado)", linewidth=2)
plt.axhline(1.0, color="k", linestyle="--", label="Valor final = 1.00")
plt.axhline(low, color="orange", linestyle=":", label=f"Inferior {visual_low_pct*100:.1f}% = {low:.3f}")
plt.axhline(high, color="orange", linestyle=":", label=f"Superior {visual_high_pct*100:.1f}% = {high:.2f}")
idx_peak = int(np.argmax(yr))
y_peak = float(yr[idx_peak])
plt.axhline(y_peak, color='red', linestyle=':', linewidth=1.5, label=f"Overshoot = {Mp:.2f}%")
if np.isfinite(Ts):
	plt.axvline(Ts, color='red', linestyle='--', linewidth=1, label=f"T_s visual = {Ts:.3f} s")
plt.title("Resposta ao degrau — PID ajustado (ts<7 s, Mp<20%)")
plt.xlabel("Tempo [s]")
plt.ylabel("Saída y(t)")
plt.grid(True, ls="--", alpha=0.6)
plt.legend()
plt.show()

import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# planta (1 / (s^2 + 5*s + 6))
num = [1]
den = [1, 5, 6]

G = ctrl.TransferFunction(num, den)
print("Planta G(s) =", G)

# controlador proporcional: Gc(s) = K

# especificações de projeto (do PDF)
TS_MAX = 10.0  # s (2%)
MP_MAX = 10.0  # %

# simulação
n_points = 2000
t_final = 100.0
t = np.linspace(0.0, t_final, n_points)

# função para achar tempo visual (2% de tolerância)
def first_persistent_time(signal, time, low, high):
	idxs = np.where((signal >= low) & (signal <= high))[0]
	if idxs.size == 0:
		return None
	for idx in idxs:
		if np.all((signal[idx:] >= low) & (signal[idx:] <= high)):
			return time[idx]
	return None

# limites visuais (98%–102%)
visual_low_pct = 0.98
visual_high_pct = 1.02
low = visual_low_pct * 1.0
high = visual_high_pct * 1.0

# sigma alvo (aprox. 2%): sigma = 4 / Ts
sigma_target = 4.0 / TS_MAX

# lugar das raízes (0 < K < ∞)
plt.figure(figsize=(7,6))
# plota o lugar das raízes; versões recentes podem não retornar tupla
ctrl.rlocus(G)

# linhas iso-ζ (constante razão de amortecimento)
def zeta_from_mp(mp_pct: float) -> float:
	mp = max(1e-9, min(99.9, mp_pct)) / 100.0
	ln_mp = np.log(mp)
	return -ln_mp / np.sqrt(np.pi**2 + ln_mp**2)

def draw_iso_zeta(ax, zeta: float, color='gray', ls='--', lw=1.0, label=None):
	zeta = np.clip(zeta, 1e-6, 0.999999)
	theta = np.arccos(zeta)                # ângulo em relação ao eixo real negativo
	phi = np.pi - theta                    # direção no 2º quadrante
	xlim = ax.get_xlim()
	x_min = min(0.0, xlim[0])
	# comprimento até alcançar x_min na projeção
	r_max = abs(x_min) / abs(np.cos(phi)) if abs(np.cos(phi)) > 1e-9 else 1.0
	r = np.linspace(0, r_max, 200)
	re = r * np.cos(phi)
	im = r * np.sin(phi)
	ax.plot(re, im, color=color, ls=ls, lw=lw, label=label)
	ax.plot(re, -im, color=color, ls=ls, lw=lw)

# ζ alvo a partir de Mp especificado
zeta_target = zeta_from_mp(MP_MAX)
ax = plt.gca()
# algumas linhas de referência
for z in [0.2, 0.4, 0.6, 0.7, 0.8]:
	if abs(z - zeta_target) < 1e-3:
		continue
	draw_iso_zeta(ax, z, color='lightgray', ls='--', lw=0.8)
# destacar a linha do alvo de overshoot
draw_iso_zeta(ax, zeta_target, color='blue', ls='-.', lw=1.5, label=f"ζ alvo (Mp≤{MP_MAX:.0f}%) ≈ {zeta_target:.3f}")
# marcar sigma (linha vertical em Re = -sigma)
ax.axvline(-sigma_target, color='green', linestyle='--', linewidth=1.2,
		   label=f"σ alvo (Ts≤{TS_MAX:.0f}s) ≈ {sigma_target:.3f}")
plt.xlabel('Re')
plt.ylabel('Im')
plt.title('Lugar das raízes — Gc(s)=K')
plt.grid(True, ls='--', alpha=0.6)
plt.legend()
plt.axvline(0, color='k', linewidth=0.8)
plt.show()

## (apenas RL — sem cálculo automático de K e sem resposta ao degrau)

# controlador integrador: Gc(s) = K/s

plt.figure(figsize=(7,6))
ctrl.rlocus(ctrl.TransferFunction([1], [1, 0]) * G)  # rlocus de Gc*G com Gc=1/s; K escala o lugar

# reutilizar linhas iso-ζ
zeta_target = zeta_from_mp(MP_MAX)
ax = plt.gca()
for z in [0.2, 0.4, 0.6, 0.7, 0.8]:
	if abs(z - zeta_target) < 1e-3:
		continue
	draw_iso_zeta(ax, z, color='lightgray', ls='--', lw=0.8)
draw_iso_zeta(ax, zeta_target, color='blue', ls='-.', lw=1.5, label=f"ζ alvo (Mp≤{MP_MAX:.0f}%) ≈ {zeta_target:.3f}")

# marcar sigma (linha vertical em Re = -sigma) também para o integrador
ax.axvline(-sigma_target, color='green', linestyle='--', linewidth=1.2,
		   label=f"σ alvo (Ts≤{TS_MAX:.0f}s) ≈ {sigma_target:.3f}")

plt.xlabel('Re')
plt.ylabel('Im')
plt.title('Lugar das raízes — Gc(s)=K/s (integrador)')
plt.grid(True, ls='--', alpha=0.6)
plt.legend()
plt.axvline(0, color='k', linewidth=0.8)
plt.show()

## (apenas RL — sem cálculo automático de K e sem resposta ao degrau)


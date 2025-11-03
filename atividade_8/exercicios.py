import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# planta (1 / (s^2 + 5*s + 6))
num = [1]
den = [1, 5, 6]

G = ctrl.TransferFunction(num, den)
print("Planta G(s) =", G)

# ----- controlador proporcional: Gc(s) = K ----- #

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
	theta = np.arccos(zeta)
	phi = np.pi - theta
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
theta_target = np.arccos(zeta_target)  # em rad
ax = plt.gca()
# algumas linhas de referência
for z in [0.2, 0.4, 0.6, 0.7, 0.8]:
	if abs(z - zeta_target) < 1e-3:
		continue
	draw_iso_zeta(ax, z, color='lightgray', ls='--', lw=0.8)
# destacar a linha do alvo de overshoot
draw_iso_zeta(ax, zeta_target, color='orange', ls='-.', lw=1.5, label=f"θ = {theta_target:.3f}")
# sigma pela relação de 2ª ordem: θ = arccos(ζ), σ = -ζ ω_n, com ω_n ≈ 4/(ζ Ts)
omega_n_target = 4.0 / (zeta_target * TS_MAX)
sigma_target = - zeta_target * omega_n_target
ax.axvline(sigma_target, color='red', linestyle='--', linewidth=1.2,
		   label=f"σ = {sigma_target:.3f}")
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.title('Lugar das raízes — Gc(s)=K')
plt.grid(True, ls='--', alpha=0.6)
plt.legend()
plt.axvline(0, color='k', linewidth=0.8)
plt.show()

# ----- controlador integrador: Gc(s) = K/s ----- #

plt.figure(figsize=(7,6))
ctrl.rlocus(ctrl.TransferFunction([1], [1, 0]) * G)  # rlocus de Gc*G com Gc=1/s; K escala o lugar

# reutilizar linhas iso-ζ
zeta_target = zeta_from_mp(MP_MAX)
theta_target = np.arccos(zeta_target)  # em rad
ax = plt.gca()
for z in [0.2, 0.4, 0.6, 0.7, 0.8]:
	if abs(z - zeta_target) < 1e-3:
		continue
	draw_iso_zeta(ax, z, color='lightgray', ls='--', lw=0.8)
draw_iso_zeta(ax, zeta_target, color='orange', ls='-.', lw=1.5, label=f"θ = {theta_target:.3f}")
# sigma pela relação de 2ª ordem também para o integrador
omega_n_target = 4.0 / (zeta_target * TS_MAX)
sigma_target = - zeta_target * omega_n_target
ax.axvline(sigma_target, color='red', linestyle='--', linewidth=1.2,
		   label=f"σ = {sigma_target:.3f}")

plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.title('Lugar das raízes — Gc(s)=K/s (integrador)')
plt.grid(True, ls='--', alpha=0.6)
plt.legend()
plt.axvline(0, color='k', linewidth=0.8)
plt.show()

# ----- controlador PI: Gc(s) = K (1 + 1/s) = K (s+1)/s ----- #

plt.figure(figsize=(7,6))
G_pi_base = ctrl.TransferFunction([1, 1], [1, 0]) * G  # (s+1)/s * G(s); K escala o lugar
ctrl.rlocus(G_pi_base)

# reutilizar linhas iso-ζ
zeta_target = zeta_from_mp(MP_MAX)
theta_target = np.arccos(zeta_target)  # em rad
ax = plt.gca()
for z in [0.2, 0.4, 0.6, 0.7, 0.8]:
	if abs(z - zeta_target) < 1e-3:
		continue
	draw_iso_zeta(ax, z, color='lightgray', ls='--', lw=0.8)
draw_iso_zeta(ax, zeta_target, color='orange', ls='-.', lw=1.5, label=f"θ = {theta_target:.3f}")

# sigma pela relação de 2ª ordem também para o PI
omega_n_target = 4.0 / (zeta_target * TS_MAX)
sigma_target = - zeta_target * omega_n_target
ax.axvline(sigma_target, color='red', linestyle='--', linewidth=1.2, label=f"σ = {sigma_target:.3f}")

plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.title('Lugar das raízes — Gc(s)=K(1 + 1/s) (PI)')
plt.grid(True, ls='--', alpha=0.6)
plt.legend()
plt.axvline(0, color='k', linewidth=0.8)
plt.show()



# ----- Respostas ao degrau em malha fechada (P, I, PI) no mesmo gráfico ----- #

K_P = 10.38   # ganho para controlador proporcional Gc=K
K_I = 3.567   # ganho para integrador Gc=K/s
K_PI = 8.402  # ganho para PI Gc=K(1 + 1/s)

# Controladores
Gc_P = ctrl.TransferFunction([K_P], [1])
Gc_I = ctrl.TransferFunction([K_I], [1, 0])                 # K/s
Gc_PI = ctrl.TransferFunction([K_PI, K_PI], [1, 0])         # K*(s+1)/s

# Malhas fechadas T(s) = feedback(Gc*G, 1)
T_P = ctrl.feedback(Gc_P * G, 1)
T_I = ctrl.feedback(Gc_I * G, 1)
T_PI = ctrl.feedback(Gc_PI * G, 1)

# Vetor de tempo comum já definido acima: t
yP_t, yP = ctrl.step_response(T_P, T=t)
yI_t, yI = ctrl.step_response(T_I, T=t)
yPI_t, yPI = ctrl.step_response(T_PI, T=t)

def compute_metrics(y: np.ndarray, time: np.ndarray, tol: float = 0.02):
	# valor final pela média no trecho de cauda (mais robusto a pequenas oscilações)
	n_tail = max(10, int(0.05 * len(y)))
	y_final = float(np.mean(y[-n_tail:]))
	y_max = float(np.max(y))
	denom = abs(y_final) if abs(y_final) > 1e-12 else 1.0
	mp_pct = max(0.0, (y_max - y_final) / denom * 100.0)
	low_b = (1.0 - tol) * y_final
	high_b = (1.0 + tol) * y_final
	ts = first_persistent_time(y, time, low_b, high_b)
	return y_final, mp_pct, ts

yf_P, mp_P, ts_P = compute_metrics(yP, yP_t)
yf_I, mp_I, ts_I = compute_metrics(yI, yI_t)
yf_PI, mp_PI, ts_PI = compute_metrics(yPI, yPI_t)

def fmt_ts(ts_val):
	return f"{ts_val:.2f}s" if ts_val is not None else f"> {t[-1]:.0f}s"

plt.figure(figsize=(8,5))
plt.plot(yP_t, yP, label=f"P (K={K_P:.2f}) — Mp={mp_P:.1f}%  Ts={fmt_ts(ts_P)}")
plt.plot(yI_t, yI, label=f"I (K={K_I:.2f}) — Mp={mp_I:.1f}%  Ts={fmt_ts(ts_I)}")
plt.plot(yPI_t, yPI, label=f"PI (K={K_PI:.2f}) — Mp={mp_PI:.1f}%  Ts={fmt_ts(ts_PI)}")
plt.axhline(1.0, color='k', ls=':', lw=1.0, label='Referência = 1')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída y(t)')
plt.title('Respostas ao degrau em malha fechada (P, I, PI)')
plt.grid(True, ls='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()


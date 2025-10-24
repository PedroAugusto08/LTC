import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# numerador e denominador
num = [1]
den = [1, 6, 5, 0]
G = ctrl.TransferFunction(num, den)

# simulação
n_points = 1000
t_final = 50.0
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

# manter Kcr e Pcr para a sintonia do PID
# controlador PID por Ziegler–Nichols
Kp_pid = 0.6 * Kcr
Ti_pid = 0.5 * Pcr
Td_pid = 0.125 * Pcr
Ki_pid = Kp_pid / Ti_pid
Kd_pid = Kp_pid * Td_pid

Cpid = ctrl.TransferFunction([Kd_pid, Kp_pid, Ki_pid], [1, 0])
Gcl_pid = ctrl.feedback(Cpid * G, 1)
# resposta ao degrau
t_pid, y_pid = ctrl.step_response(Gcl_pid, T=t)
# métricas
y_inf_pid = float(y_pid[-1])
Mp_pid = (np.max(y_pid) - 1.0) / 1.0 * 100.0
ts_vis_pid = first_persistent_time(y_pid, t_pid, low, high)
if ts_vis_pid is None:
	idx_pid = np.where(y_pid >= low)[0]
	ts_vis_pid = float(t_pid[idx_pid[0]]) if idx_pid.size else None

print("\nCom PID:")
print(f"Kp={Kp_pid:.6f}, Ti={Ti_pid:.6f}, Td={Td_pid:.6f}, Ki={Ki_pid:.6f}, Kd={Kd_pid:.6f}")
print(f"y(∞) ≈ {y_inf_pid:.6f}")
print(f"M_p ≈ {Mp_pid:.4f}%")
print(f"T_s vis ≈ {ts_vis_pid if ts_vis_pid is not None else np.nan}")

# gráfico resposta com PID
plt.figure(figsize=(9,5))
plt.plot(t_pid, y_pid, label="G(s) com PID", linewidth=2)
plt.axhline(1.0, color="k", linestyle="--", label="Valor final = 1.00")
plt.axhline(low, color="orange", linestyle=":", label=f"Inferior {visual_low_pct*100:.1f}% = {low:.3f}")
plt.axhline(high, color="orange", linestyle=":", label=f"Superior {visual_high_pct*100:.1f}% = {high:.2f}")
idx_peak_pid_plot = int(np.argmax(y_pid))
y_peak_pid_plot = float(y_pid[idx_peak_pid_plot])
plt.axhline(y_peak_pid_plot, color='red', linestyle=':', linewidth=1.5, label=f"Overshoot = {Mp_pid:.2f}%")
if ts_vis_pid is not None:
	plt.axvline(ts_vis_pid, color='red', linestyle='--', linewidth=1, label=f"T_s visual = {ts_vis_pid:.3f} s")
plt.title("Resposta ao degrau — Com PID")
plt.xlabel("Tempo [s]")
plt.ylabel("Saída y(t)")
plt.grid(True, ls="--", alpha=0.6)
plt.legend()
plt.show()

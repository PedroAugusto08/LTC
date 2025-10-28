import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# numerador e denominador
num = [1]   # 1
den = [1, 6, 5, 0]   # s^3 + 6 s^2 + 5 s
G = ctrl.TransferFunction(num, den)
print("Planta G(s) =", G)

# malha fechada sem controlador
Gcl = ctrl.feedback(G, 1)

# simulação
n_points = 30000
t_final = 300.0
t = np.linspace(0, t_final, n_points)
t_out, y_out = ctrl.step_response(Gcl, T=t)

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

# valor final aproximado, overshoot e tempo de acomodação visual
y_inf = float(y_out[-1])
Mp = (np.max(y_out) - 1.0) / 1.0 * 100.0
ts_vis = first_persistent_time(y_out, t_out, low, high)

print("\nResultados da malha fechada sem controlador (realimentação unitária):")
print(f"Valor final estimado y(∞) ≈ {y_inf:.6f}")
print(f"Overshoot M_p ≈ {Mp:.4f} %")
print(f"Tempo de acomodação visual (≈2%) t_s ≈ {ts_vis:.3f} s")

# plot
plt.figure(figsize=(9,5))
plt.plot(t_out, y_out, label="G(s) fechado (resposta)", linewidth=2)
plt.axhline(1.0, color="k", linestyle="--", label="Valor final = 1.00")
plt.axhline(low, color="orange", linestyle=":", label=f"Inferior {visual_low_pct*100:.2f}% = {low:.3f}")
plt.axhline(high, color="orange", linestyle=":", label=f"Superior {visual_high_pct*100:.1f}% = {high:.3f}")
# marcar overshoot (pico) com linha horizontal pontilhada
idx_peak = int(np.argmax(y_out))
t_peak = float(t_out[idx_peak])
y_peak = float(y_out[idx_peak])
plt.axhline(y_peak, color='red', linestyle=':', linewidth=1.5,
            label=f"Overshoot = {Mp:.2f}%")
plt.axvline(ts_vis, color="red", linestyle="--", label=f"T_s visual = {ts_vis:.3f} s")


plt.title("Resposta ao degrau - Malha fechada sem controlador")
plt.xlabel("Tempo [s]")
plt.ylabel("Saída y(t)")
plt.grid(True, ls="--", alpha=0.6)
plt.legend(loc='lower right')
plt.show()

# controlador PI por Ziegler–Nichols

# parâmetros
Kcr = 30.00
Pcr = 2.81

# fórmulas de ZN para PI
Kp = 0.45 * Kcr
Ti = Pcr / 1.2
Ki = Kp / Ti

print("\nProjeto PI por Ziegler–Nichols:")
print(f"Kcr = {Kcr:.2f}, Pcr = {Pcr:.2f}")
print(f"Kp = 0.45*Kcr = {Kp:.6f}")
print(f"Ti = Pcr/1.2  = {Ti:.6f}")
print(f"Ki = Kp/Ti    = {Ki:.6f}")

# controlador PI: C(s) = Kp + Ki/s = (Kp*s + Ki)/s
Cpi = ctrl.TransferFunction([Kp, Ki], [1, 0])

# malha fechada com PI
Gcl_pi = ctrl.feedback(Cpi * G, 1)

# resposta ao degrau
t_pi, y_pi = ctrl.step_response(Gcl_pi, T=t)

# métricas
y_inf_pi = float(y_pi[-1])
Mp_pi = (np.max(y_pi) - 1.0) / 1.0 * 100.0
ts_vis_pi = first_persistent_time(y_pi, t_pi, low, high)

print("\nResultados com PI:")
print(f"Valor final estimado y(∞) ≈ {y_inf_pi:.6f}")
print(f"Overshoot M_p ≈ {Mp_pi:.4f} %")
print(f"Tempo de acomodação visual (≈2%) t_s ≈ {ts_vis_pi:.3f} s")

# gráfico resposta com PI
plt.figure(figsize=(9,5))
plt.plot(t_pi, y_pi, label="G(s) com PI (resposta)", linewidth=2)
plt.axhline(1.0, color="k", linestyle="--", label="Valor final = 1.00")
plt.axhline(low, color="orange", linestyle=":", label=f"Inferior {visual_low_pct*100:.2f}% = {low:.3f}")
plt.axhline(high, color="orange", linestyle=":", label=f"Superior {visual_high_pct*100:.1f}% = {high:.3f}")
# marcar overshoot (pico) com PI com linha horizontal pontilhada
idx_peak_pi = int(np.argmax(y_pi))
t_peak_pi = float(t_pi[idx_peak_pi])
y_peak_pi = float(y_pi[idx_peak_pi])
plt.axhline(y_peak_pi, color='red', linestyle=':', linewidth=1.5,
            label=f"Overshoot = {Mp_pi:.2f}%")
plt.axvline(ts_vis_pi, color="red", linestyle="--", label=f"T_s visual = {ts_vis_pi:.3f} s")

plt.title("Resposta ao degrau - Malha fechada com PI")
plt.xlabel("Tempo [s]")
plt.ylabel("Saída y(t)")
plt.grid(True, ls="--", alpha=0.6)
plt.legend()
plt.show()

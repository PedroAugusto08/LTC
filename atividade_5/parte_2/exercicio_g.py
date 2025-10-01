import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# sistema em malha aberta
G = ctrl.tf([1.0], [1.0, 1.2, 9.0])

t = np.linspace(0, 10, 1000)

# ganhos a simular
Ks = [1, 10]

for K in Ks:
    # T = G/(1 + K*G)
    K_tf = ctrl.tf([K], [1])
    T_closed = ctrl.feedback(G, K_tf)

    # resposta ao degrau unitário
    t_out, y = ctrl.step_response(T_closed, T=t)

    # polos, parâmetros teóricos
    polos = ctrl.poles(T_closed)
    wn = np.sqrt(9.0 + K)
    zeta = 1.2 / (2.0 * wn)

    # valores em regime
    y_ss_teo = 1.0 / (9.0 + K)
    y_ss_num = float(y[-1])
    e_ss_num = 1.0 - y_ss_num

    print(f"\n=== K = {K} (realimentação) ===")
    print(f"Polos: {polos}")
    print(f"ω_n (teórico) = {wn:.4f} rad/s")
    print(f"ζ (teórico)   = {zeta:.4f}")
    print(f"y_ss (teórico) = {y_ss_teo:.6f}")
    print(f"y_ss (numérico) = {y_ss_num:.6f}")
    print(f"Erro estacionário (estimado) e_ss = {e_ss_num:.6f}")

    plt.figure(figsize=(8, 4.8))
    plt.plot(t_out, y, label=f"Saída y(t), K={K}")
    plt.axhline(y=y_ss_teo, linestyle='--', color='orange',
                label=f"y_ss teórico = {y_ss_teo:.3f}")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Saída y(t)")
    plt.title(f"Resposta ao degrau — malha fechada (K={K}, ganho na realimentação)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    fname = f"saida_g_K{K}.png"
    plt.savefig(fname, dpi=200)
    plt.close()
    print(f"Gravado: {fname}")

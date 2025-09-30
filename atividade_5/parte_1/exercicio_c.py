import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# G(s) = 1/(3 s)
G = ctrl.tf([1], [3, 0])

t = np.linspace(0, 30, 1000)

# ganhos a serem testados
Ks = [1, 10]

for K in Ks:
    # sistema em malha fechada com ganho K
    K_tf = ctrl.tf([K], [1])
    T_closed = ctrl.feedback(G, K_tf)

    # resposta ao degrau unitário
    t_out, y = ctrl.step_response(T_closed, T=t)

    # valor teórico de regime estacionário
    y_ss_teo = 1.0 / K

    # valor numérico aproximado (t_final)
    y_final_num = y[-1]

    print(f"\n=== K = {K} ===")
    print(f"y(t_final) (numérico) = {y_final_num:.6f}")
    print(f"y_ss (teórico)        = {y_ss_teo:.6f}")

    plt.figure(figsize=(8, 4.8))
    plt.plot(t_out, y, label=f"Saída y(t), K={K}")
    plt.axhline(y=y_ss_teo, linestyle='--', linewidth=1, color='orange',
                label=f"y_ss (teórico) = {y_ss_teo:.3f}")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Saída $y(t)$")
    plt.title(f"Resposta ao degrau — malha fechada (K={K})")
    plt.grid(True)
    plt.legend()
    fname_y = f"saida_K{K}.png"
    plt.tight_layout()
    plt.savefig(fname_y, dpi=200)
    plt.close()
    print(f"Gravado: {fname_y}")
    

# Figura comparativa (caso (c): ganho K no feedback)
plt.figure(figsize=(8, 4.8))
for K in Ks:
    K_tf = ctrl.tf([K], [1])
    T_closed = ctrl.feedback(G, K_tf)
    t_out, y = ctrl.step_response(T_closed, T=t)
    y_ss = 1.0 / K
    plt.plot(t_out, y, label=f"K={K} (y_ss={y_ss:.2f})")
    plt.axhline(y_ss, linestyle='--', linewidth=0.8, color='gray')

plt.xlabel("Tempo (s)")
plt.ylabel("Saída y(t)")
plt.title("Comparação respostas — ganho K no feedback")
plt.grid(True)
plt.legend()
plt.ylim(0, 1.05)  # mostra bem K=1 (y_ss=1) e K=10 (y_ss=0.1)
plt.tight_layout()
plt.savefig("comparacao_respostas_feedback.png", dpi=200)
plt.close()
print("Gravado: comparacao_respostas_feedback.png")
# ...existing code...

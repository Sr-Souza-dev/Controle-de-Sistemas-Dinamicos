import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import mplcursors

# Definindo a Função que plota o diagrama de bode
def PlotarBode(mag, phase, w, title):
    fig, axs = plt.subplots(2, sharex=True)
    lines0 = axs[0].semilogx(w,20*np.log10(mag))
    axs[0].grid(which='both', axis='both')
    axs[0].set_ylabel('Amplitude')
    axs[0].set_title('Diagrama de Bode ' + title)
    mplcursors.cursor(lines0)
    lines1 = axs[1].semilogx(w,180*phase/np.pi)
    axs[1].grid(which='both', axis='both')
    axs[1].set_ylabel('Fase')
    axs[1].set_xlabel('Frequência')
    mplcursors.cursor(lines1)

# Sistema malha aberta (Vermelho)
plt.close('all')
num1 = [1]
den1 = [1,2.2,1.4,2]
G_s = ctrl.TransferFunction(num1,den1)
ts, ys = ctrl.step_response(G_s)
print(G_s)

# Sistema realimentado (Verde)
G_scl1 = ctrl.feedback(G_s, sys2=1, sign=-1)
tcls1, ycls1 = ctrl.step_response(G_scl1,ts)

# Sistema realimentado com compensador/controlador (Azul)
K = 0.522
C_s = ctrl.series(ctrl.TransferFunction([1,0.2,1],[1,0.85]),ctrl.TransferFunction([1],[1,0.1]))
KG = ctrl.series(ctrl.series(K,C_s),G_s)
G_scl = ctrl.feedback(KG, sys2=1, sign=-1)
tcls, ycls = ctrl.step_response(G_scl,ts)

# Plotagem dos três sistemas acima
plt.figure(0)
plt.title("Analise das malhas")
plt.plot(ts,ys,'r',tcls,ycls,'b',tcls1,ycls1,'g')
plt.grid(True)

# vermelho  -> malha aberta
# verde     -> malha fechada
# Azul      -> malha fechada com compensador


# # Lugar geometrico das raizes (LGR) sem compensador/controlador
# plt.figure(1)
# ctrl.rlocus(G_s)

# Lugar geometrico das raizes (LGR) com compensador/controlador
plt.figure(2)
ctrl.rlocus(KG)

# Diagrama de Bode do sistema em malha aberta
mag, phase, w = ctrl.bode_plot(G_s,plot=False)
PlotarBode(mag, phase, w, "Malha Aberta")

# # Diagrama de Bode do sistema em malha fechada
# mag1, phase1, w1 = ctrl.bode_plot(G_scl1,plot=False)
# PlotarBode(mag1, phase1, w1, "Malha Fechada")

# # Diagrama de Bode do sistema em malha fechada compensado
# mag2, phase2, w2 = ctrl.bode_plot(G_scl,plot=False)
# PlotarBode(mag2, phase2, w2, "Malha Fechada (Compensado)")

plt.show()
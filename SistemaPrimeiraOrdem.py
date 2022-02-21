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

# Sistema em malha aberta (gráfico vermelho)
plt.close('all')
num1 = [0.1]
den1 = [1, 0.2, 0] 
G_s = ctrl.TransferFunction(num1,den1)
ts, ys = ctrl.step_response(G_s)

# Sistema realimentado (gráfico verde)
G_scl1 = ctrl.feedback(G_s, sys2=1, sign=-1)
tcls1, ycls1 = ctrl.step_response(G_scl1,ts)

# Sistema realimentado com compensador/controlador (gráfico azul)
C_s = ctrl.series(2,ctrl.TransferFunction([3.875,1],[0.461,1]))
print(C_s)
KG = ctrl.series(C_s,G_s)
G_scl = ctrl.feedback(KG, sys2=1, sign=-1)
tcls, ycls = ctrl.step_response(G_scl,ts)

# Plotagem dos três sistemas acima
plt.figure(0)
plt.title("Analise das malhas")
plt.plot(ts,ys,'r',tcls,ycls,'b',tcls1,ycls1,'g')
plt.grid(True)

# Cores dos graficos na plotagem
# vermelho  -> malha aberta
# verde     -> malha fechada
# azul      -> malha fechada com compensador

# Lugar geometrico das raizes (LGR)
plt.figure(1)
plt.title("LGR - Malha Aberta")
ctrl.root_locus(G_s, print_gain=True)
plt.ylim([-3,3]); plt.xlim([-3,3])

# Diagrama de Bode do sistema em malha aberta (função integrada)
mag, phase, w = ctrl.bode_plot(G_s,plot=False)
PlotarBode(mag, phase, w, "Malha Aberta")

# # Diagrama de Bode do sistema em malha fechada
# mag1, phase1, w1 = ctrl.bode_plot(G_scl1,plot=False)
# PlotarBode(mag1, phase1, w1, "Malha Fechada")

# Diagrama de Bode do sistema em malha fechada compensado
mag2, phase2, w2 = ctrl.bode_plot(G_scl,plot=False)
PlotarBode(mag2, phase2, w2, "Malha Fechada (Compensado)")

plt.show()
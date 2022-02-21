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
ts = np.arange(0,200,0.5)
ts, ys = ctrl.step_response(G_s,ts)

K = 3           # Ganho para atender KP

# Plotando diagrama de BODE do sistema (com ganho)
mag, phase, w = ctrl.bode_plot(ctrl.series(1,G_s),plot=False)
PlotarBode(mag, phase, w, "sem Ganho")

# Variaveis descoberdas para projeto do controlador em atraso
wn   = 1.023            # De acordo com a fase desejada (130º)
magn = 16.0679
v    = wn/10
tau  = 1/v
beta = 10**(magn/20)

print("Tau: ",tau)
print("beta: ",beta)

# Sistema controlado (Azul)
C_s = ctrl.series(K,ctrl.TransferFunction([tau,1],[beta*tau,1]))
KG = ctrl.series(C_s,G_s)
G_scl = ctrl.feedback(KG, sys2=1, sign=-1)
tcls, ycls = ctrl.step_response(G_scl,ts)

# Plotando diagrama de BODE do sistema (com compensador)
mag2, phase2, w2 = ctrl.bode_plot(KG,plot=False)
PlotarBode(mag2, phase2, w2, "compensado")

# Sistema realimentado (Verde)
G_scl1 = ctrl.feedback(G_s, sys2=1, sign=-1)
tcls1, ycls1 = ctrl.step_response(G_scl1,ts)

# Plotagem dos três sistemas acima
plt.figure(0)
plt.title("Analise das malhas")
plt.plot(ts,ys,'r',tcls,ycls,'b',tcls1,ycls1,'g')
# vermelho  -> malha aberta
# verde     -> malha fechada
# Azul      -> malha fechada com compensador

plt.show()
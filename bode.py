import matplotlib.pyplot as plt
import control as ctrl
import numpy as np
import mplcursors

plt.close('all')

def PlotarBode(mag, phase, w):
    fig, axs = plt.subplots(2, sharex=True)
    lines0 = axs[0].semilogx(w,20*np.log10(mag))
    axs[0].grid(which='both', axis='both')
    axs[0].set_ylabel('Amplitude')
    axs[0].set_title('Diagrama de Bode')
    mplcursors.cursor(lines0)
    lines1 = axs[1].semilogx(w,180*phase/np.pi)
    axs[1].grid(which='both', axis='both')
    axs[1].set_ylabel('Fase')
    axs[1].set_xlabel('Frequência')
    mplcursors.cursor(lines1)

# Sistema
G = ctrl.TransferFunction([4], [1, 2, 0])
mag, phase, w = ctrl.bode_plot(G,plot=False)
PlotarBode(mag, phase, w)

K = 10
G1 = ctrl.series(K,G)
mag1, phase1, w1 = ctrl.bode_plot(G1,plot=False)
PlotarBode(mag1, phase1, w1)

# Compensador
Kc = 46
C = ctrl.TransferFunction([1, 4.2663],[1, 19.6242])

# Malha fechada
CG = ctrl.series(Kc,C,G)
mag2, phase2, w2 = ctrl.bode_plot(CG,plot=False)
PlotarBode(mag2, phase2, w2)
CGcl = ctrl.feedback(CG)
CGclnc = ctrl.feedback(G)

# Resposta a entrada degrau 
T = np.linspace(0,10,100)
tnc, ync = ctrl.step_response(CGclnc,T)
tcl, ycl = ctrl.step_response(CGcl,T)
plt.figure()
plt.plot(tcl, ycl,'b',tnc,ync,'r')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.title('Resposta ao degrau sistema compensado e não compensado')
plt.grid()
plt.show()
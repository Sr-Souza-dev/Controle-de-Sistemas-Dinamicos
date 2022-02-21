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

# ------    REQUISITOS ------    
# 10% Overshoot
# 10s Tempo de acomodação (Ts)
# Erro de estado estacionário nulo

#-------------- SISTEMA ---------------
num = [230]
den = [1,0.512,2.622]
G_s = ctrl.TransferFunction(num,den)

# ------ Sistema malha aberta (vermelho) -----
#ts = np.arange(0,200,0.5)
ts, ys = ctrl.step_response(G_s)

# ------ Sistema malha fechada (verde) -----
G_scl = ctrl.feedback(G_s, sys2=1, sign=-1)
tcls, ycls = ctrl.step_response(G_scl,ts)

# ------ Sistema malha fechada - Controlado LGR (azul) -----
K_LGR = 0.001411
C_LGR = ctrl.TransferFunction(den,[1,0.798,0]) * K_LGR
G_LGR = ctrl.series(C_LGR,G_s)
G_scl1 = ctrl.feedback(G_LGR, sys2=1, sign=-1)
tcls1, ycls1 = ctrl.step_response(G_scl1,ts)

# Plotagem LGR 
# plt.figure(1)
# ctrl.rlocus(G_s)
# plt.figure(2)
# ctrl.rlocus(G_LGR)

# ------ Sistema malha fechada - Controlador dominio da Frequência (preto) -----
overshoot = 10
Ts = 10
Kc = 1
zeta = -np.log(overshoot/100) / (np.sqrt(np.pi**2 + (np.log(10/100))**2))
MF = zeta * 100
MFCtrl = MF - (180 - 178) + 8 
MFCtrlRad = MFCtrl * np.pi / 180
a = (1 - np.sin(MFCtrlRad)) / (1 + np.sin(MFCtrlRad))
ampDes = 20 * np.log10(Kc/np.sqrt(a))
wn = 7.29589
T = 1 / (np.sqrt(a) * wn)

print("MF: ",MF, ";  MFCTRL", MFCtrl,";     a: ",a, ";      ampDes: ",ampDes,";     T:",T, "\n\n")

# Controlador Analise em frequência
C_SF = Kc * ctrl.TransferFunction([T,1], [T*a,1])
print(C_SF)
G_SFC = ctrl.series(C_SF,G_s)
G_sclF = ctrl.feedback(G_SFC, sys2=1, sign=-1)
tclsF, yclsF = ctrl.step_response(G_sclF,ts)

# Plotando diagrama de bode não compensado
mag, phase, w = ctrl.bode_plot(G_s,plot=False)
PlotarBode(mag, phase, w, "Não Compensado")

# Plotando diagrama de bode compensado
mag, phase, w = ctrl.bode_plot(G_SFC,plot=False)
PlotarBode(mag, phase + (360 * np.pi / 180), w, "Compensado")

# # ------------ Plotagem dos sistemas --------------
# plt.figure(0)
# plt.title("Malha aberta")
# plt.plot(ts,ys,'r')
# plt.grid(True)

# plt.figure(1)
# plt.title("Malha fechada")
# plt.plot(tcls,ycls,'g')
# plt.grid(True)

# plt.figure(2)
# plt.title("Compensado LGR")
# plt.plot(tcls1,ycls1,'b')
# plt.grid(True)

plt.figure(3)
plt.title("Analise das respostas")
plt.plot(tcls,ycls,'g',tclsF,yclsF,'k', tcls1,ycls1,'b')
plt.grid(True)
# black -> compensador por analise de fase
# blue -> compensador por LGR
# green -> Malha Fechada

plt.show()
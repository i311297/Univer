import numpy as np
import math
from tkinter import *
import matplotlib
# matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinter import N,S,E,W
from tkinter import messagebox


def F(u, t):
    return np.sin(0.1*u+t)


def solve(D,N,dt,NT):
    x = np.linspace(0,2*math.pi,N)
    u0 = np.sin(5*x)
    fu = np.fft.fft(u0)
    u = u0
    z=np.empty((NT,N), dtype=float)
    h= 2*math.pi/N

    l = np.zeros(N)
    for k in range(N//2):
        l[k] = 4*D*(np.sin(k*h/4))**2/h**2
        l[-k] = l[k]
    
    for t in range(1, N):  
        us = u
        fus = fu 
        for s in range(5):
            F1 = F(u, (t-1)*dt)
            F2 = F(us, t*dt)
            f = np.fft.fft(F1+F2)
            fus = ((2-dt*l)*fu + dt*f)/(2 + dt*l)
            us = np.fft.ifft(fus)
        z[t] = np.real(us)
        u = us
        fu = fus
        
    return z

window = Tk()
window.title('Уравнение диффузии в кольце')
w = 750
h = 850 
ws = window.winfo_screenwidth() 
hs = window.winfo_screenheight() 
window.configure(background='white')
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.resizable(0, 0)
bgc = '#B0C4DE'
def click():
    # try:
        D = float(txtD.get())
        NN = int(txtN.get())
        NT = int(txtNT.get())
        DT = float(txtDt.get())
        sol = solve(D,NN,DT,NT)
        fs = (5,4)
        try:
            frame1.grid_remove()
        except:
            pass        

        if r_var.get()==1:
            from tkinter import N,S,E,W

            frame1 = Frame(window,height=600,width=w,bg = 'white')
            frame1.grid(column = 0, row = 0,sticky = W+N+S+E)
#             fig = Figure(figsize=fs, dpi=100)
#             fig.add_subplot(111).imshow(sol[1:].transpose())
#             fig.colorbar()
#             canvas = FigureCanvasTkAgg(fig, master=frame1)  # A tk.DrawingArea.
#             canvas.draw()
#             canvas.get_tk_widget().grid(column = 0, row = 0,rowspan=4)
            
            
            fig, ax1 = plt.subplots(figsize=(6,6), ncols=1)
            pos = ax1.imshow(sol.T)
            fig.colorbar(pos, ax=ax1)
            # plt.close(fig) 
            canvas = FigureCanvasTkAgg(fig, master=frame1)  
            canvas.draw()
            frame1.grid_propagate(0)
            canvas.get_tk_widget().grid(column = 0, row = 0,rowspan=4,ipadx = 65)
        elif r_var.get()==0:
            from tkinter import N,S,E,W
            frame1 = Frame(window,height=600,width=w,bg = 'white')
            frame1.grid(column = 0, row = 0,sticky = W+N+S+E)
            # fig = Figure(figsize=(6,5), dpi=100)
            # fig.add_subplot(111).plot(sol[1:].T)
            # canvas = FigureCanvasTkAgg(fig, master=frame1)
            # canvas.draw()
            # canvas.get_tk_widget().grid(column = 0, row = 0,rowspan=4)
            # frame1.grid_propagate(0)
            def animate(i):
                line.set_ydata(sol[i])  # update the data
                return line,
            fig = plt.Figure()
            x = np.linspace(0, 2*math.pi, NN)
            canvas = FigureCanvasTkAgg(fig, master=frame1)
            canvas.get_tk_widget().grid(column=0,row=1,ipadx = 65,ipady = 30)
            ax = fig.add_subplot(111)
            line, = ax.plot(x, sol[0])
            ax.set_ylim([-1.1, 1.1])
            ani = animation.FuncAnimation(fig, animate, np.arange(1,NN), interval=10, blit=False)
            frame1.grid_propagate(0)
        window.mainloop()
            

            
            
           
            


            



        
        
    # except:
    #     messagebox.showerror('error', message = 'Неверные значения параметров')



frame1 = Frame(window,height=600,width=w,bg = 'white')
frame2 = Frame(window, width = w, bd=1, relief=SUNKEN,bg = bgc)
frame3 = Frame(frame2,bg=bgc)
txtD = Entry(frame2, width = 5, justify='center', font=("Calibri Bold",15))
txtN = Entry(frame2, width = 5, justify='center', font=("Calibri Bold",15))
txtNT = Entry(frame2, width = 5, justify='center', font=("Calibri Bold",15))
txtDt = Entry(frame2, width = 5, justify='center', font=("Calibri Bold",15))
# txtF = Entry(frame3, width = 15, justify='center', font=("Calibri Bold",15))
labD = Label(frame2, text='Коэффициент диффузии, D', font=("Calibri Bold",15), bg = bgc)
labN = Label(frame2, text='Количество узлов сетки, N', font=("Calibri Bold",15), bg = bgc)
labDt = Label(frame2, text='Шаг по времени, dt', font=("Calibri Bold",15), bg = bgc)
labNT = Label(frame2, text='Число шагов по времени, NT', font=("Calibri Bold",15), bg = bgc)
# labF =  Label(frame3, text='Функция', font=("Calibri Bold",20), bg = bgc)
r_var = BooleanVar()
r_var.set(0)
r1 = Radiobutton(frame3,text='Анимация профиля волны', variable=r_var, value=0,font=("Calibri Bold",15),bg = bgc)
r2 = Radiobutton(frame3,text='Тепловая карта', variable=r_var, value=1,font=("Calibri Bold",15),bg = bgc)
but = Button(frame3, text = 'Поехали!',font=("Calibri Bold",18),width = 18, command = click, bg = '#ADD8E6')



#place
frame1.grid(column = 0, row = 0,sticky = W+N+S+E)
frame2.grid(column = 0, row = 1)
txtD.grid(column = 1, row = 0,pady = 11, ipady = 3)
txtN.grid(column = 1, row = 1, pady = 11, ipady = 3)
txtNT.grid(column = 1, row = 2, pady = 11, ipady = 3)
txtDt.grid(column = 1, row = 3, pady = 11, ipady = 3)
labD.grid(column = 0, row =0, pady = 11, padx = 3)
labN.grid(column = 0, row =1, pady = 11, padx = 3)
labNT.grid(column = 0, row =2, pady = 11, padx = 3)
labDt.grid(column = 0, row =3, pady = 11, padx = 3)
frame3.grid(column = 2,row = 0,rowspan=4,sticky = W+N+S+E)

# labF.grid(column=0,row=0,padx =150,pady = 5)
# txtF.grid(column=0,row=1, ipady = 3,pady = 10)
r1.grid(column = 0, row = 3,sticky = W,padx = 30)
r2.grid(column = 0, row = 4,sticky = W, padx = 30)

but.grid(column = 0, row = 5,pady = 15, ipady = 5)

frame2.configure(height=250,width=w)
frame2.grid_propagate(0)


    

window.mainloop()
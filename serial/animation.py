#---------Imports

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#---------End of imports



from tkinter import Frame,Label,Entry,Button


class Window(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def Clear(self):
        print("clear")
        self.textAmplitude.insert(0, "1.0")
        self.textSpeed.insert(0, "1.0")


    def Plot(self):
        self.v = float(self.textSpeed.get())
        self.A = float(self.textAmplitude.get())


    def animate(self,i):
        self.line.set_ydata(self.A*np.sin(self.x+self.v*i))  # update the data
        return self.line,


    def init_window(self):
        self.master.title("Use Of FuncAnimation in tkinter based GUI")
        self.pack(fill='both', expand=1)

        #Create the controls, note use of grid

        self.labelSpeed = Label(self,text="Speed (km/Hr)",width=12)
        self.labelSpeed.grid(row=0,column=1)
        self.labelAmplitude = Label(self,text="Amplitude",width=12)
        self.labelAmplitude.grid(row=0,column=2)

        self.textSpeed = Entry(self,width=12)
        self.textSpeed.grid(row=1,column=1)
        self.textAmplitude = Entry(self,width=12)
        self.textAmplitude.grid(row=1,column=2)

        self.textAmplitude.insert(0, "1.0")
        self.textSpeed.insert(0, "1.0")
        self.v = 1.0
        self.A = 1.0


        self.buttonPlot = Button(self,text="Plot",command=self.Plot,width=12)
        self.buttonPlot.grid(row=2,column=1)

        self.buttonClear = Button(self,text="Clear",command=self.Clear,width=12)
        self.buttonClear.grid(row=2,column=2)


        self.buttonClear.bind(lambda e:self.Clear)



        tk.Label(self,text="SHM Simulation").grid(column=0, row=3)

        self.fig = plt.Figure()

        self.x = 20*np.arange(0, 2*np.pi, 0.01)        # x-array


        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot(self.x, np.sin(self.x))


        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(column=0,row=4)


        self.ani = animation.FuncAnimation(self.fig, self.animate, np.arange(1, 200), interval=25, blit=False)

root = tk.Tk()
root.geometry("700x400")
app = Window(root)
tk.mainloop()
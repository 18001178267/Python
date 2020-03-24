import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox  # 要使用messagebox先要导入模块
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
 
# 第1步，实例化object，建立窗口window
window = tk.Tk()
 
# 第2步，给窗口的可视化起名字
window.title('异常地质监测')
 
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('800x600')  # 这里的乘是小x
 
l = tk.Label(window, text='仪器编号', bg='white', font=('Arial', 12), width=30, height=20)
l.place(x=750,y=550)

fig = Figure(figsize=(10, 6), dpi=100)
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

x = np.arange(-5.0, 5.0, 0.02)
   
y_s1 = np.sin(x)
y_s2 = np.sin(x*2)
y_s3 = np.sin(x*3)

 # initialize drawing
try:
    l1, = ax1.plot(x, y_s1)
except:
    pass
try:
    l2, = ax2.plot(x, y_s2)
except:
    pass
try:
    l3, = ax3.plot(x, y_s3)
except:
    pass
canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



# 第6步，主窗口循环显示
window.mainloop()

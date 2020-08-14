from tkinter import *

root = Tk()
sw = root.winfo_screenwidth()                             # 获取屏幕宽度
sh = root.winfo_screenheight()                            # 获取屏幕高度
root.geometry('+{}+{}'.format((sw-460)//2, (sh-400)//2))  # 窗口居中
root.title('Python聊天群')                                 # 设置窗口标题

frameT = Frame(root, width=460, height=320)               # 顶部容器(root为父容器)
frameT.pack(expand='yes', fill='both')
frameB = Frame(root, width=460, height=80)                # 底部容器(root为父容器)
frameB.pack(expand='yes', fill='both')

Output = Text(frameT)                                     # 显示文本框(frameT为父容器)
Output.pack(expand='yes', fill='both')
Input = Text(frameB, height=6)                            # 输入文本框(frameB为父容器)
Input.pack(expand='yes', fill='both')

btnFrame = Frame(frameB, height=24, bg='White')           # 按钮容器(frameB为父容器)
btnFrame.pack(expand='yes', fill='both')

# 发送按钮(btnFrame为父容器)
Button(btnFrame, text='发送', width=8, bg='DodgerBlue', fg='White').pack(side=RIGHT)

root.mainloop()                                           # 窗口主循环

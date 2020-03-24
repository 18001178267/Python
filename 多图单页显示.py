import numpy as np
import matplotlib.pyplot as plt
from pylab import *

x = np.arange(-5.0, 5.0, 0.02)
y1 = np.sin(x)

plt.figure()
plt.subplot(1,2,1)
plt.plot(x, y1)

plt.subplot(1,2,2)
#设置x轴范围
xlim(-2.5, 2.5)
#设置y轴范围
ylim(-1, 1)
plt.plot(x, y1)
#plt.pause(1)
plt.show()

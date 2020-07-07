
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
file = '6.txt'
data = np.loadtxt(file, delimiter='\t', skiprows=1000)
x = data[20200:21200]
y= x.reshape(-1,1)
km = KMeans(n_clusters=2)
km.fit(y)
print(km.cluster_centers_)
plt.plot(range(0,len(x)),x)
plt.show()



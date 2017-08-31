import numpy as np
import matplotlib.pyplot as plt 

x = np.linspace(0,10,11)

y = np.tanh(x/2.0)

plt.plot(x,y,'ro',markersize=3)
plt.show()
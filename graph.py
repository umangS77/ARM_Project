import matplotlib.pyplot as plt
import numpy as np 

X = ['BMS1_spmf.txt', 'BMS2_spmf.txt', 'MSNBC.txt']
  
N = 3
ind = np.arange(N) 
width = 0.25
heightdif = 0.08
fig, ax = plt.subplots() 
  
xvals = [0.092, 0.181, 4.912]

for i, v in enumerate(xvals):
    ax.text(i-0.05, v + heightdif, str(v), color='black')

bar1 = ax.bar(ind, xvals, width, color = 'r')
  
yvals = [1.296, 3.932, 3.425]

for i, v in enumerate(yvals):
    ax.text(i + (width) - 0.05, v + heightdif, str(v), color='black')

bar2 = ax.bar(ind+width, yvals, width, color='g')
  
zvals = [0.302, 0.530, 0.676]

for i, v in enumerate(zvals):
    ax.text(i + (width*2) -0.05, v + heightdif, str(v), color='black')

bar3 = ax.bar(ind+width*2, zvals, width, color = 'b')
  
plt.xlabel("Dataset")
plt.ylabel("Runtime in seconds")
plt.title("For Minimum Support = 10%")
  
ax.set_xticks(ind+width)
ax.set_xticklabels(X, minor=False)
plt.legend( (bar1, bar2, bar3), ('Basic Apriori', 'Apriori with Hash Mapping', 'FP Growth') )
plt.show()

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

BD_Ratio = np.loadtxt('data2.csv', delimiter=',')
p = np.loadtxt('p2.csv', delimiter=',')

Data = np.loadtxt('Particle_Data.csv',delimiter=',')

x = np.zeros(len(Data))
y = np.zeros(len(Data))
for i in range(len(Data)):
    x[i] = Data[i,0]
    y[i] = Data[i,1]

# Create ScatterPlot
fig = plt.figure()
ax=plt.gca()
#ax.scatter(BD_Ratio,p,c="blue",alpha=0.95,edgecolors='none', label='data')
ax.scatter(x,y,c="red",alpha=0.95,edgecolors='none', label='data')
ax.set_yscale('log')
ax.set_xscale('log')

def PowerFunc(x, a, b):
    return a * np.power(x, b)

def R_squared(xdata,ydata,popt,pcov):
	residuals = ydata - PowerFunc(xdata, *popt)
	ss_res = np.sum(residuals**2)
	ss_tot = np.sum((ydata-np.mean(ydata))**2)
	length = len(BD_Ratio)
	r_squared = 1 - (ss_res / ss_tot)
	return r_squared

length = len(BD_Ratio)
Startpos = length

'''
for i in range(length-2,0,-2):
    Xval =  x[i:Startpos]
    Yval = y[i:Startpos]
    popt, pcov = curve_fit(PowerFunc,Xval,Yval)
    R2 = R_squared(Xval,Yval,popt,pcov)
    print(R2)
    if R2 < 0.90:
        Startpos = i
        plt.plot(Xval, PowerFunc(Xval, *popt), color = 'k', label=)

Startpos = length'''

for i in range(length-2,0,-2):
    Xval =  x[i:Startpos]
    Yval = y[i:Startpos]
    popt, pcov = curve_fit(PowerFunc,Xval,Yval)
    R2 = R_squared(Xval,Yval,popt,pcov)
    print(R2)
    if R2 < 0.98:
        Startpos = i
        plt.plot(Xval, PowerFunc(Xval, *popt), color = 'b', label=popt[1])


plt.plot(Xval, PowerFunc(Xval, *popt),color = 'k', label=popt)
plt.xlabel('B/D')
plt.ylabel('P/D')
plt.legend()
plt.show()
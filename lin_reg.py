import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

BD_Ratio = np.loadtxt('data.csv', delimiter=',')
p = np.loadtxt('p.csv', delimiter=',')


fig = plt.figure()
ax=plt.gca()
ax.scatter(BD_Ratio,p,c="blue",alpha=0.95,edgecolors='none', label='data')
ax.set_yscale('log')
ax.set_xscale('log')

def ExpFunc(x, a, b):
    return a * np.power(x, b)

'''
popt, pcov = curve_fit(ExpFunc, BD_Ratio, p)
plt.plot(newX, ExpFunc(newX, *popt), 'r-', 
         label="({0:.3f}*x**{1:.3f})".format(*popt))
print ("Exponential Fit: y = (a*(x**b))")
print ("\ta = popt[0] = {0}\n\tb = popt[1] = {1}".format(*popt))
'''

def R_squared(xdata,ydata,popt,pcov):
	residuals = ydata - ExpFunc(xdata, *popt)
	ss_res = np.sum(residuals**2)
	ss_tot = np.sum((ydata-np.mean(ydata))**2)
	length = len(BD_Ratio)
	r_squared = 1 - (ss_res / ss_tot)
	return r_squared

length = len(BD_Ratio)
for i in range(2,length):
    Xval =  BD_Ratio[0:i]
    Yval = p[0:i]
    #newX = np.linspace(BD_Ratio[i],BD_Ratio[0],i)
    #print(BD_Ratio[i],BD_Ratio[0])
    popt, pcov = curve_fit(ExpFunc,Xval, Yval)
    plt.plot(Xval, ExpFunc(Xval, *popt), 'r-', label="({0:.3f}*x**{1:.3f})".format(*popt))
    R2 = R_squared(Xval,Yval,popt,pcov)
    print(R2)
'''		if R2 < 0.98:
		BD_Ratio = BD_Ratio[i:length]
		p = p[i:length]
'''	

plt.show()
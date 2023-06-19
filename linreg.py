import numpy as np
import matplotlib.pyplot as plt

Data = np.loadtxt('Particle_Data.csv',delimiter=',')
x = np.zeros(len(Data))
y = np.zeros(len(Data))
for i in range(len(Data)):
    x[i] = Data[i,0]
    y[i] = Data[i,1]

def R_squared(xdata,ydata,pred_y):
	residuals = ydata - pred_y
	ss_res = np.sum(residuals**2)
	ss_tot = np.sum((ydata-np.mean(ydata))**2)
	r_squared = 1 - (ss_res / ss_tot)
	return r_squared


length = len(x)
Startpos = length
fig, ax1 = plt.subplots(1, 1, figsize=(8,6))

count = 0
for i in range(length-2,0,-2):
	Xval =  x[i:Startpos]
	Yval = y[i:Startpos]
	coefs = np.polyfit(np.log(Xval), np.log(Yval), 1)
	pred_y = np.multiply((np.log(Xval)), coefs[0]) + coefs[1]
	R2 = R_squared(np.log(Xval),np.log(Yval),pred_y)
	print(R2)
	count += 1 
	if R2 < 0.998 :
		if count >= 5:
			Startpos = i
			ax1.plot((Xval), np.exp(pred_y), 'k--', label = coefs[0]) # exponentiate pred_y
			count = 0

ax1.scatter(x, y) # original scale!
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.legend()
plt.show()

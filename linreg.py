import numpy as np
import matplotlib.pyplot as plt

x = np.loadtxt('data2.csv', delimiter=',')
y = np.loadtxt('p2.csv', delimiter=',')

def R_squared(xdata,ydata,pred_y):
	residuals = ydata - pred_y
	ss_res = np.sum(residuals**2)
	ss_tot = np.sum((ydata-np.mean(ydata))**2)
	r_squared = 1 - (ss_res / ss_tot)
	return r_squared

length = len(x)
Startpos = length
fig, ax1 = plt.subplots(1, 1, figsize=(8,6))

'''
count = 0
i = length - 2
while i >= 0:
	Xval =  x[i:Startpos]
	Yval = y[i:Startpos]
	coefs = np.polyfit(np.log(Xval), np.log(Yval), 1)
	pred_y = np.multiply((np.log(Xval)), coefs[0]) + coefs[1]
	R2 = R_squared(np.log(Xval),np.log(Yval),pred_y)
	print(R2)
#	count += 1
	if R2 < 0.94 :
#		if count >= 5:
		Startpos = i
		ax1.plot((Xval), np.exp(pred_y), 'k--', label = coefs[0]) # exponentiate pred_y
#			count = 0
		i -=2
	else:
		i -=1
'''
ax1.scatter(x, y) # original scale!

for i in range(len(x)):
    ax1.annotate(i, (x[i], y[i]),color = 'r')

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.legend()
plt.show()

line1 = input('Between which points do you want the first linear regression (Write both points with a comma inbetween)\n')
line2 = input('Between which points do you want the second linear regression (Write both points with a comma inbetween)\n')
pt1,pt2 = line1.split(',')
pt3,pt4 = line2.split(',')

print('b_m/D = ' , x[int(pt2)])
print('p/D - 2 = ' , y[int(pt2)] - 2)

Xval =  x[int(pt1):int(pt2)]
Yval = y[int(pt1):int(pt2)]

fig, ax1 = plt.subplots(1, 1, figsize=(8,6))
ax1.scatter(x, y) # original scale!

ax1.set_xscale('log')
ax1.set_yscale('log')

coefs = np.polyfit(np.log(Xval), np.log(Yval), 1)
pred_y = np.multiply((np.log(Xval)), coefs[0]) + coefs[1]
ax1.plot((Xval), np.exp(pred_y), 'k--', label = (coefs[0]))
R2 = R_squared(np.log(Xval),np.log(Yval),pred_y)
print('R2 = ', R2)

print('slope of line 1 = ' , coefs[0])
Xval =  x[int(pt3):int(pt4)]
Yval = y[int(pt3):int(pt4)]

coefs = np.polyfit(np.log(Xval), np.log(Yval), 1)
pred_y = np.multiply((np.log(Xval)), coefs[0]) + coefs[1]
ax1.plot((Xval), np.exp(pred_y), 'k--', label = (coefs[0]))
R2 = R_squared(np.log(Xval),np.log(Yval),pred_y)
print('R2 = ', R2)

print('slope of line 2 = ' , coefs[0])

plt.legend()
plt.show()

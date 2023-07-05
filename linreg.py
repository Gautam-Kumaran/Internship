import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('ASTM 3.csv',delimiter=',')
x1,y1 = [],[]

for i in range(len(data)):
	x1.append(data[i,0])
	y1.append(data[i,1])

fig, ax1 = plt.subplots(1, 1, figsize=(8,6))
ax1.scatter(x1, y1, color = 'g') # original scale!

x = np.loadtxt('data2.csv', delimiter=',')
y = np.loadtxt('p2.csv', delimiter=',')
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

print('((p/D) at b_m) - 2 = ' , y[int(pt2)] - 2)

print('M = ' , 1.14/( y[int(pt2)] - 2) )

Xval =  x[int(pt1):int(pt2)]
Yval = y[int(pt1):int(pt2)]

fig, ax1 = plt.subplots(1, 1, figsize=(8,6))

ax1.scatter(x1, y1, color = 'g') # original scale!
ax1.scatter(x, y) # original scale!

ax1.set_xscale('log')
ax1.set_yscale('log')

coefs = np.polyfit(np.log(Xval), np.log(Yval), 1)
pred_y = np.multiply((np.log(Xval)), coefs[0]) + coefs[1]
ax1.plot((Xval), np.exp(pred_y), 'k--', label = (coefs[0]))

print('slope of line 1 = ' , coefs[0])
Xval =  x[int(pt3):int(pt4)]
Yval = y[int(pt3):int(pt4)]

coefs = np.polyfit(np.log(Xval), np.log(Yval), 1)
pred_y = np.multiply((np.log(Xval)), coefs[0]) + coefs[1]
ax1.plot((Xval), np.exp(pred_y), 'k--', label = (coefs[0]))

print('slope of line 2 = ' , coefs[0])

plt.legend()
plt.show()
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
import cv2


data = np.loadtxt('ASTM1DATA.csv',delimiter=',')
x,y = [],[]

for i in range(len(data)):
	x.append(data[i,0])
	y.append(data[i,1])

def R_squared(ydata,pred_y):
	residuals = ydata - pred_y
	ss_res = np.sum(residuals**2)
	ss_tot = np.sum((ydata-np.mean(ydata))**2)
	r_squared = 1 - (ss_res / ss_tot)
	return r_squared

fig, ax1 = plt.subplots(1, 1, figsize=(8,6))
ax1.scatter(x, y, color = 'y', label = 'Guida et al. (2019)') # original scale!

x1 = np.loadtxt('data.csv', delimiter=',')
y1 = np.loadtxt('p.csv', delimiter=',')
ax1.scatter(x1, y1, color = 'r', label = 'Alshibli') # original scale!


for i in range(len(x1)):
    ax1.annotate(i, (x1[i], y1[i]),color = 'r')

ax1.set_xlim(0.001,1)
ax1.set_ylim(2)
ax1.set_xlabel('$\it{b}$/D',fontsize = 14,fontfamily = 'Times New Roman')
ax1.set_ylabel('$\it{p}$/D',fontsize = 14,fontfamily = 'Times New Roman')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.tick_params(axis = 'both', direction = 'in',which = 'both')
ax1.set_xticks([0.001,0.01,0.1,1],[0.001,0.01,0.1,1],fontsize = 14,fontfamily = 'Times New Roman')
ax1.set_yticks([2,3,4,5,6],[2,3,4,5,6],fontsize = 14,fontfamily = 'Times New Roman')

ax1.legend(prop = matplotlib.font_manager.FontProperties(family = 'Times New Roman', size = 14),frameon = False)
plt.savefig('my_plot.png')
plt.show()
plot = cv2.imread('my_plot.png')



line1 = input('Between which points do you want the first linear regression (Write both points with a comma inbetween)\n')
pt1,pt2 = line1.split(',')

def linecreate(Xval,Yval):
	coefs = np.polyfit(np.log(Xval), np.log(Yval), 1)
	pred_y = np.multiply((np.log(Xval)), coefs[0]) + coefs[1]
	r2 = R_squared(Yval,np.exp(pred_y))
	return pred_y,r2,coefs

while True:
	Xval1 =  x1[int(pt1):int(pt2)+1]
	Yval1 = y1[int(pt1):int(pt2)+1]
	pred_y1,r21,coefs1 = linecreate(Xval1,Yval1)
	print('Rquared Value = ',r21)
	r2ok = input('Is the R_Squared value for line1 good?(y or n)\n')
	if r2ok == 'y':
		break
	else:
		cv2.imshow('plot',plot)
		cv2.waitKey(0)
		line1 = input('Between which points do you want the first linear regression (Write both points with a comma inbetween)\n')
		pt1,pt2 = line1.split(',')

line2 = input('Between which points do you want the second linear regression (Write both points with a comma inbetween)\n')
pt3,pt4 = line2.split(',')

while True:
	Xval2 =  x1[int(pt3):int(pt4)+1]
	Yval2 = y1[int(pt3):int(pt4)+1]
	pred_y2,r22,coefs2 = linecreate(Xval2,Yval2)
	print('Rquared Value = ',r22)
	r2ok = input('Is the R_Squared value for line2 good?(y or n)\n')
	if r2ok == 'y':
		break
	else:
		cv2.imshow('plot',plot)
		cv2.waitKey(0)
		line2 = input('Between which points do you want the first linear regression (Write both points with a comma inbetween)\n')
		pt3,pt4 = line1.split(',')


fig, ax1 = plt.subplots(1, 1, figsize=(8,6))

ax1.scatter(x, y, color = 'r', label = 'Guida et al. (2019)') # original scale!
ax1.scatter(x1, y1, label = 'Present Study',) # original scale!

ax1.set_xscale('log')
ax1.set_yscale('log')

ax1.plot((Xval1), np.exp(pred_y1), 'k--', label = (coefs1[0]))

ax1.plot((Xval2), np.exp(pred_y2), 'k--', label = (coefs2[0]))


print('\n((p/D) at b_m) - 2 = ' , y1[int(pt2)] - 2)

print('M = ' , 1.14/( y1[int(pt2)] - 2),'\n')

ax1.set_xlim(0.001,1)
ax1.set_ylim(2)
ax1.set_xlabel('$\it{b}$/D',fontsize = 14,fontfamily = 'Times New Roman')
ax1.set_ylabel('$\it{p}$/D',fontsize = 14,fontfamily = 'Times New Roman')
ax1.tick_params(axis = 'both', direction = 'in',which = 'both')
ax1.set_xticks([0.001,0.01,0.1,1],[0.001,0.01,0.1,1],fontsize = 14,fontfamily = 'Times New Roman')
ax1.set_yticks([2,3,4,5,6],[2,3,4,5,6],fontsize = 14,fontfamily = 'Times New Roman')
ax1.legend(prop = matplotlib.font_manager.FontProperties(family = 'Times New Roman', size = 14),frameon = False)
plt.show()
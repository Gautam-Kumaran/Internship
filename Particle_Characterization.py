import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


#Store the PNG image
image = cv2.imread('CROPPED.png')

#Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Use Otsu's method to determine the optimal threshold value
_ , thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

#Save binarized image
cv2.imwrite('Binarized_image.png', thresh)

# find the largest contour in the threshold image
cnts,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
c = max(cnts, key=cv2.contourArea)

for x in range(len(thresh)):
	for y in range(len(thresh[x])):
		thresh[x,y] = 0

for i in range(len(c)):
	x = c[i,0,0]
	y= c[i,0,1]
	thresh[y,x] = 255
cv2.imwrite("Original Contour2.png", thresh)

print(len(c))

def distance_calculation(point1,point2):
	return(((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**(1/2))*1.04

# Reshape the contour to a 2D array of coordinates
contour = c.squeeze()

area = cv2.contourArea(c)*1.0816
print(area)
beginning_distance = (math.sqrt((4*area)/math.pi))
distance = beginning_distance 
p = []
BD_Ratio = []
count = np.zeros(len(c))
check = 0

while True:
	sum = 0
	perimeter = np.zeros(len(c))
	for i in range(len(c)):
		currentpoint =  c[i,0]
		for j in range(len(c)):
			if (distance_calculation(currentpoint,c[j,0])>=distance):
				perimeter[i] = perimeter[i] + distance_calculation(currentpoint,c[j,0])
				currentpoint = c[j,0]
		perimeter[i] = perimeter[i]+ distance_calculation(currentpoint, c[j,0])
	print(min(perimeter),'----',min(perimeter)/beginning_distance)
	p.append((min(perimeter))/beginning_distance)
	BD_Ratio.append(distance/beginning_distance)
	distance = distance * 0.8
	if p[len(p)-1]==p[len(p)-2]:
		check += 1
		if check==4:
			break

BD_Ratio = np.array(BD_Ratio)
p = np.array(p)

np.savetxt('data.csv', BD_Ratio, delimiter=',')
np.savetxt('p.csv', p, delimiter=',')

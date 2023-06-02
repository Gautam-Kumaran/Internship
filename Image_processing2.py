import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

#Store the PNG image
image = cv2.imread('New_Particle.png')

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
distance = (math.sqrt((4*area)/math.pi))*0.8
beginning_distance = distance
perimeter = []
BD_Ratio = []
count = np.zeros(len(c))

while True:
	sum = 0
	count = np.zeros(len(c))
	for i in range(len(c)):
		currentpoint =  c[i,0]
		for j in range(len(c)):
			if (distance_calculation(currentpoint,c[j,0])>=distance):
				currentpoint = c[j,0]
				count[i] = count[i] + 1
		count[i] = count[i] + 1 
	print(min(count),'-----',distance,'-----',distance/beginning_distance)
	perimeter.append(min(count))
	BD_Ratio.append(distance/beginning_distance)
	distance = distance * 0.8
	if min(count)==len(c):
		break

fig, ax = plt.subplots()
ax.plot(BD_Ratio,perimeter)
ax.set_yscale('log')
ax.set_xscale('log')
plt.show()
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Store the PNG image
image = cv2.imread('toyura PARTICLE CROPPED.png')
# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def gamma_correction(image, gamma):
    # Normalize pixel values
    normalized_image = image / 255.0

    # Apply gamma correction
    corrected_image = np.power(normalized_image, 1 / gamma)

    # Denormalize pixel values
    corrected_image = (corrected_image * 255).astype(np.uint8)

    return corrected_image

# Apply gamma correction with gamma = 1.8
gamma_value = 2.5
corrected_image = gamma_correction(gray, gamma_value)

cv2.imwrite('gamma_image.png', corrected_image)

# Use Otsu's method to determine the optimal threshold value
_ , thresh = cv2.threshold(corrected_image, 0, 255, cv2.THRESH_OTSU)

# Save binarized image
cv2.imwrite('Binarized_image.png', thresh)

# Find the largest contour in the threshold image
cnts,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
c = max(cnts, key=cv2.contourArea)

# Make image full black
for x in range(len(thresh)):
	for y in range(len(thresh[x])):
		thresh[x,y] = 0

# Make only biggest contour white
for i in range(len(c)):
	x = c[i,0,0]
	y= c[i,0,1]
	thresh[y,x] = 255
cv2.imwrite("Original Contour2.png", thresh)

print(len(c))

# Distance Formula
def length_calculation(point1,point2):
	return(((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**(1/2))*1.04

# Reshape the contour to a 2D array of coordinates
# contour = c.squeeze()

area = cv2.contourArea(c)*1.0816
print(area)
Diameter = (math.sqrt((4*area)/math.pi))
Stick_Length = Diameter
p = []
BD_Ratio = []
count = np.zeros(len(c))
check = 0

# While loop to repeat for different stick lengths
while True:
	sum = 0
	# Store perimeter with each different inital point
	perimeter = np.zeros(len(c))
	# For loop to find perimeter for each initial point
	for i in range(len(c)):
		currentpoint =  c[i,0]
		# For loop to move through all points on boundary
		for j in range(len(c)):
			if (length_calculation(currentpoint,c[j,0])>=Stick_Length):
				perimeter[i] = perimeter[i] + length_calculation(currentpoint,c[j,0])
				currentpoint = c[j,0]
		perimeter[i] = perimeter[i]+ length_calculation(currentpoint, c[j,0])
	print(np.mean(perimeter),'----',np.mean(perimeter)/Diameter)
	# Storing P/D and B/D
	p.append((np.mean(perimeter))/Diameter)
	BD_Ratio.append(Stick_Length/Diameter)
	# Reducing stick length
	Stick_Length = Stick_Length * 0.8
	if p[len(p)-1]==p[len(p)-2]:
		check += 1
		if check==4:
			break

BD_Ratio = np.array(BD_Ratio)
p = np.array(p)

np.savetxt('data.csv', BD_Ratio, delimiter=',')
np.savetxt('p.csv', p, delimiter=',')
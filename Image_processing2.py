import cv2
import numpy as np
import argparse
import imutils

#Store the PNG image
image = cv2.imread('New_Particle.png')

#Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Use Otsu's method to determine the optimal threshold value
_ , thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

#Save binarized image
cv2.imwrite('Binarized_image.png', thresh)

# find the largest contour in the threshold image
cnts,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
c = max(cnts, key=cv2.contourArea)

for x in range(len(thresh)):
    for y in range(len(thresh[x])):
        thresh[x,y] = 0

# draw the shape of the contour on the output image, compute the
# bounding box, and display the number of points in the contour

output = thresh.copy()
cv2.drawContours(output, [c], -1, (255), 1)
cv2.imwrite("Original Contour.png", output)

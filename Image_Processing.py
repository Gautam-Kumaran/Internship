import cv2
import numpy as np

#Store the PNG image
image = cv2.imread('New_Particle.png')

#Convert the image to grayscal//e
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Use Otsu's method to determine the optimal threshold value
_ , threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

#Determine if pixel is boundary by checking if any of surrounding pixels are black and assign boundary pixels to Outline(array)
outline = []
for i in range(len(threshold)):
    for j in range(len(threshold[i])):
        if(threshold[i,j]==255):
            if(threshold[i-1,j]==0 or threshold[i+1,j]==0 or threshold[i,j+1]==0 or threshold[i,j-1]==0 or threshold[i-1,j+1]==0 or threshold[i+1,j+1]==0 or threshold[i+1,j-1]==0 or threshold[i-1,j-1]==0):
                outline.append([i,j])

#Make all pixel values have intensity 0(i.e make all pixels black)
for i in range(len(threshold)):
    for j in range(len(threshold[i])):
        threshold[i,j] = 0

#Using Outline(array) make boundary pixels have intensity 255(i.e make only boundary pixels white)
for k in range(len(outline)):
    m,n = outline[k]
    threshold[m,n] = 255

#Step 4: Save the binarized and outlined image as a new PNG file
cv2.imwrite('Outline_image.png', threshold)
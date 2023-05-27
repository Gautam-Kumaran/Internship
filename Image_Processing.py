import cv2
import numpy as np

#Store the PNG image
image = cv2.imread('New_Particle.png')

#Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Use Otsu's method to determine the optimal threshold value
_ , threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

cv2.imwrite('Binarized_image.png', threshold)

#Determine if pixel is boundary by checking if any of surrounding pixels are black and assign boundary pixels to Outline(array)

outline = []
for x in range(len(threshold)):
    for y in range(len(threshold[x])):
        if(threshold[x,y]==255):
            xval = [x,x-1,x+1]
            yval = [y,y-1,y+1]
            for i in xval:
                for j in yval:
                    if(threshold[i,j]==0):
                        outline.append([x,y])

#Make all pixel values have intensity 0(i.e make all pixels black)
for x in range(len(threshold)):
    for y in range(len(threshold[x])):
        threshold[x,y] = 0

#Using Outline(array) make boundary pixels have intensity 255(i.e make only boundary pixels white)
for i in range(len(outline)):
    x,y = outline[i]
    threshold[x,y] = 255

#Save the binarized and outlined image as a new PNG file
cv2.imwrite('Outline_image.png', threshold)

#Find all shapes(multiple pixels connected to each other)
_ , labels, stats, _ = cv2.connectedComponentsWithStats(threshold, connectivity=8)

# Find the index of the largest connected component
largest_component_index = np.argmax(stats[1:, cv2.CC_STAT_AREA]) +1

# Make only the largest connected component white
mask = np.where(labels == largest_component_index, 255, 0)

# Save the resulting image
cv2.imwrite("result.png", mask)
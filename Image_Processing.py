import cv2
import numpy as np

#Step 1: Store the PNG image
image = cv2.imread('New_Particle.png')

#Step 2: Convert the image to grayscal//e
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Step 3: Use Otsu's method to determine the optimal threshold value
_ , threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)


count = 0
outline = []

firstvalue = True
for i in range(len(threshold)):
    for j in range(len(threshold[i])):
        if(threshold[i,j]==255):
            if(threshold[i-1,j]==0 or threshold[i+1,j]==0 or threshold[i,j+1]==0 or threshold[i,j-1]==0 or threshold[i-1,j+1]==0 or threshold[i+1,j+1]==0 or threshold[i+1,j-1]==0 or threshold[i-1,j-1]==0):
                outline.append([i,j])
                count+=1


#for i in range(len(threshold)):
for i in range(len(threshold)):
    for j in range(len(threshold[i])):
        print(i,j)
        for k in range(len(outline)):
            if outline[k] == [i,j]:
                threshold[i,j]=255
                break
            else: threshold[i,j]=0

#Step 4: Save the binarized image as a new PNG file
cv2.imwrite('binarized_image.png', threshold)
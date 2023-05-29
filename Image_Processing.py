import cv2
import numpy as np

def next_8_connected_point(oldpoints,currentpoint,mask,Startpoint):
    x,y = currentpoint
    coords = [[x-1,y],[x-1,y+1],[x,y+1],[x+1,y+1],[x+1,y],[x+1,y-1],[x,y-1],[x-1,y-1]]
    for i in range(len(coords)):
        x,y = coords[i]
        if (mask[x,y]==255):
            newpoint = True
            if coords[i]==Startpoint:
                return oldpoints,[0,0]
            for l in range(len(oldpoints)):
                if coords[i]==oldpoints[l]:
                    newpoint = False
            if newpoint==True :
                oldpoints.append(currentpoint)
                return oldpoints,coords[i]
    for k in range(len(oldpoints)):
        if(currentpoint==oldpoints[k]):
            return oldpoints,currentpoint
    oldpoints.append(currentpoint)
    return oldpoints,currentpoint

def Find_Beginning_Piece(stats,mask):
    top = stats[1]
    for i in range(stats[0],(stats[0]+stats[3])):
        if(mask[top,i]==255):
            return[top,i]

#Store the PNG image
image = cv2.imread('New_Particle.png')

#Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Use Otsu's method to determine the optimal threshold value
_ , threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

#Save binarized image
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
                        break

#Make all pixel values have intensity 0(i.e make all pixels black)
for x in range(len(threshold)):
    for y in range(len(threshold[x])):
        threshold[x,y] = 0

#Using Outline(array) make boundary pixels have intensity 255(i.e make only boundary pixels white)
for i in range(len(outline)):
    x,y = outline[i]
    threshold[x,y] = 255

#Save the outlined image as a new PNG file
cv2.imwrite('Outline_image.png', threshold)

#Find all shapes(multiple pixels connected to each other)
_ , labels, stats , _ = cv2.connectedComponentsWithStats(threshold, connectivity=8)

#Find the index of the largest connected component
largest_component_index = np.argmax(stats[1:, cv2.CC_STAT_AREA]) +1

#Make only the largest connected component white
mask = np.where(labels == largest_component_index, 255, 0).astype(np.uint8)

#Save the resulting image
cv2.imwrite("result.png", mask)

oldpoints = []
currentpoint = Find_Beginning_Piece(stats[1], mask)
clockwisemovement = []
initialpoint=currentpoint
oldpoints , currentpoint = next_8_connected_point(oldpoints, currentpoint, mask, initialpoint)
R = 100
while initialpoint != currentpoint:
    prevpoint = currentpoint
    oldpoints , currentpoint = next_8_connected_point(oldpoints, currentpoint, mask, initialpoint)
    if currentpoint == [0,0]:
        break
    if(currentpoint==prevpoint):
        
        i = len(oldpoints)-1
        while(prevpoint==currentpoint):
            prevpoint = oldpoints[i]
            oldpoints , currentpoint = next_8_connected_point(oldpoints, oldpoints[i], mask, initialpoint)
            i -= 1
    clockwisemovement.append(currentpoint)
    x,y=currentpoint
    mask[x,y] = R
    cv2.imwrite("resultcheck.png", mask)
    R+=1



print(clockwisemovement)

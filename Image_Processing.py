import cv2
import numpy as np

#Code to check for the next point connected to current point

def next_8_connected_point(oldpoints,currentpoint,mask,Startpoint):
    x,y = currentpoint
#8 point CO-ORDINATES
    coords = [[x-1,y],[x-1,y+1],[x,y+1],[x+1,y+1],[x+1,y],[x+1,y-1],[x,y-1],[x-1,y-1]]
    
    for i in range(len(coords)):
#Executes the following code for one of the 8point co-ord
        x,y = coords[i]
#Checks if co-ord is a boundary point
        if (mask[x,y]==255):
            newpoint = True
#if one of the surrounding points is the Starting point, returns 0,0. Since code moves clockwise, the second point will not register the first point
            if coords[i]==Startpoint:
                return oldpoints,[0,0]
#Makes sure the selected co-ord is not a repeated point
            for l in range(len(oldpoints)):
                if coords[i]==oldpoints[l]:
                    newpoint = False
#If the co-ord is boundary and also not a repeated point, the current point gets added to the oldpoints list and return the oldpoint list and the selected co-ord
            if newpoint==True :
                oldpoints.append(currentpoint)
                return oldpoints,coords[i]
#If none of the 8point co-ords fit the conditions, then check if the current point is already on the oldpoints list. If yes then just return oldpoints list and the current point
    for k in range(len(oldpoints)):
        if(currentpoint==oldpoints[k]):
            return oldpoints,currentpoint
#If the current point is not on the oldpoints list, then add it to the list and then return the list and the current point
    oldpoints.append(currentpoint)
    return oldpoints,currentpoint

#Finds the piece to start from
def Find_Beginning_Piece(stats,mask):
#Finds the highest X Value where there is a boundary point
    top = stats[1]
#Finds the first point from the left at the Highest X value that belongs on the boundary
    for i in range(stats[0],(stats[0]+stats[3])):
        if(mask[top,i]==255):
#Return the point
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

#Initialise variables and lists
oldpoints = []
currentpoint = Find_Beginning_Piece(stats[1], mask)
clockwisemovement = []
initialpoint=currentpoint
R = 100

while True:
#Store previous point value
    prevpoint = currentpoint
#Update currentpoint value
    oldpoints , currentpoint = next_8_connected_point(oldpoints, currentpoint, mask, initialpoint)
#If currentpoint is returned as 0,0 that means it has arrived back to the initial point and so we stop the code
    if currentpoint == [0,0]:
        break
#If the condition is true, this means that no surrounding point is a new boundary point. Hence we backtrack till we find a new boundary point in the surroundings
    if(currentpoint==prevpoint):
        i = len(oldpoints)-1
#Code keeps checking previous points until we find a new point. 
        while(prevpoint==currentpoint):
            prevpoint = oldpoints[i]
            oldpoints , currentpoint = next_8_connected_point(oldpoints, oldpoints[i], mask, initialpoint)
            i -= 1
#We append the new point to the array
    clockwisemovement.append(currentpoint)
#Small checking section to create a new image that shows the movement by increasing intensity through each traversed point
    x,y=currentpoint
    mask[x,y] = R
    cv2.imwrite("resultcheck.png", mask)
    R+=1

print(clockwisemovement)
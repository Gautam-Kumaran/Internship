import cv2

image = cv2.imread('COLGROUT 1.png',0)

'''
hist_equal = cv2.equalizeHist(image)
cv2.imshow('original image',image)
cv2.imshow('equalised image',hist_equal)
cv2.imwrite('equalised image.png',hist_equal)
'''

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
equalized = clahe.apply(image)

cv2.imwrite('equalised image2.png',equalized)


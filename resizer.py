import cv2
image = cv2.imread('pictures/back.jpg')
image = cv2.resize(image, (32, 32))
cv2.imwrite('pictures/back.jpg', image)

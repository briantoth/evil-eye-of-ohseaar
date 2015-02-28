import cv2
image = cv2.imread('HDR.jpg')

crop_image = image[100:300, 125:1300]
cv2.imwrite('gray_image.tif', crop_image)


import cv2
import numpy as np
from matplotlib import pyplot as plt

# загрузка изображения
img = cv2.imread('Foto-sobaki-2.jpg', cv2.IMREAD_GRAYSCALE)

# оператор Собеля для определения границ
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
sobel = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)

# фильтр Гаусса для уменьшения шума
gaussian = cv2.GaussianBlur(img, (5, 5), 0)

# вывод результатов
plt.subplot(2, 2, 1), plt.imshow(img, cmap='gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(2, 2, 2), plt.imshow(sobel, cmap='gray')
plt.title('Sobel'), plt.xticks([]), plt.yticks([])
plt.subplot(2, 2, 3), plt.imshow(gaussian, cmap='gray')
plt.title('Gaussian'), plt.xticks([]), plt.yticks([])
plt.subplot(2, 2, 4), plt.hist(img.ravel(), 256)
plt.title('Histogram'), plt.xlim([0, 256])
plt.show()

# детектор углов Харриса
gray = np.float32(img)
harris = cv2.cornerHarris(gray, 2, 3, 0.04)
harris = cv2.dilate(harris, None)


# преобразование формы массива
harris_color = cv2.cvtColor(harris, cv2.COLOR_GRAY2RGB)
harris_color[harris > 0.01 * harris.max()] = [0, 0, 255]

# вывод результатов
plt.imshow(harris_color)
plt.title('Harris corners')
plt.show()

# детектор углов Shi-Tomasi
corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
corners = np.intp(corners)

# нормализуем изображение до диапазона [0, 1]
img_norm = cv2.normalize(img, None, 0, 1, cv2.NORM_MINMAX, cv2.CV_32F)

for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y), 3, 255, -1)

# вывод результатов
plt.imshow(img)
plt.title('Shi-Tomasi corners')
plt.show()

# функция label
ret, labels = cv2.connectedComponents(img)

# вывод результатов
print(f'Number of objects: {ret-1}')
plt.imshow(labels)
plt.title('Connected components')
plt.show()

# Определение центров масс объектов с помощью пороговой бинаризации
gray = cv2.convertScaleAbs(gray)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
centers = []
for contour in contours:
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centers.append((cX, cY))

# Детекция SIFT-особенностей
sift = cv2.SIFT_create()
kp = sift.detect(gray, None)
img = cv2.drawKeypoints(img, kp, img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Отрисовка углов Харриса красным цветом
img[harris > 0.01 * harris.max()] = [0, 0, 255]

# Отрисовка центров масс объектов зеленым цветом
for center in centers:
    cv2.circle(img, center, 5, (0, 255, 0), -1)

# Отрисовка областей SIFT голубым цветом
img = cv2.drawKeypoints(img, kp, None, color=(255, 0, 0))

# Отображение изображения
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

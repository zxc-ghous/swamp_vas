import numpy as np
import matplotlib.pyplot as plt
import cv2
import rasterio


def remove_small_contours(matrix: np.uint8, area_size=1000):
    contours, _ = cv2.findContours(matrix, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    selected_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > area_size:
            selected_contours.append(contour)
            blank_image = np.zeros(matrix.shape, np.uint8)
            cv2.fillPoly(blank_image, pts=selected_contours, color=(255, 255, 255))
    return blank_image


def put_area(matrix):
    ret, thresh = cv2.threshold(matrix, 1, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    for i, cnt in enumerate(contours):
        M = cv2.moments(cnt)
        if M['m00'] != 0.0:
            x1 = int(M['m10'] / M['m00'])
            y1 = int(M['m01'] / M['m00'])
        area = cv2.contourArea(cnt)
        cv2.putText(matrix, f'Area :{area}', (x1 - 150, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return matrix


if __name__ == '__main__':
    fig, ax = plt.subplots(1, 3)
    ndwi_dataset = rasterio.open(r'data/ndwi.tiff').read()[:, :1000, :1000]
    sparse_ndwi = np.uint8(np.where(ndwi_dataset > 0.1, ndwi_dataset, -1).reshape((1000, 1000, 1)))
    test = remove_small_contours(sparse_ndwi, 1000)
    ax[1].imshow(put_area(test))
    ax[1].set_title('NDWI+remove small contours+area')
    ax[0].imshow(sparse_ndwi)
    ax[0].set_title('NDWI threshold 0.1')
    ax[2].imshow(ndwi_dataset[0])
    ax[2].set_title('NDWI')
    plt.show()

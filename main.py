import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from rasterio import plot
import numpy as np


def area_water(matrix, threshold=0.1, spatial_res=10.0):
    '''accepts only matrix with ndwi filter'''
    boolean_matrix = np.where(matrix > threshold, 1, 0)
    return (boolean_matrix.sum() * spatial_res)


def area(matrix, spatial_res=10.0):
    match len(matrix.shape):
        case 2:
            return (matrix.shape[0] * matrix.shape[1]) * spatial_res
        case 3:
            return (matrix.shape[1] * matrix.shape[2]) * spatial_res


if __name__ == '__main__':
    fig, ax = plt.subplots(1, 2)
    rgb_dataset = rasterio.open(r'data/rgb.tiff').read([1, 2, 3])[:, :1000, :1000]
    ndwi_dataset = rasterio.open(r'data/ndwi.tiff').read(1)[:1000, :1000]

    show(rgb_dataset, ax=ax[0])
    show(ndwi_dataset, ax=ax[1])
    fig.colorbar(ax[1].imshow(ndwi_dataset))
    plt.show()

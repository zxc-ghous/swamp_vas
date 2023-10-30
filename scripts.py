import rasterio
import numpy as np
import os

dir_path = r'C:\Users\SCII5\PycharmProjects\pythonProject\data\S2B_MSIL1C_20231019T062859_N0509_R077_T43UCB_20231019T081708.SAFE\GRANULE\L1C_T43UCB_A034566_20231019T063044\IMG_DATA'
red_path = os.path.join(dir_path, r'T43UCB_20231019T062859_B04.jp2')
green_path = os.path.join(dir_path, r'T43UCB_20231019T062859_B03.jp2')
blue_path = os.path.join(dir_path, r'T43UCB_20231019T062859_B02.jp2')
nir_path = os.path.join(dir_path, r'T43UCB_20231019T062859_B08.jp2')


def normalize(band):
    band_min, band_max = (band.min(), band.max())
    return ((band - band_min) / (band_max - band_min))


def brighten(band):
    alpha = 0.06  # Contrast control
    beta = 0  # Brightness control
    return np.clip(alpha * band + beta, 0, 255)


def get_ndwi():
    band_green = rasterio.open(green_path)
    band_nir = rasterio.open(nir_path)
    ndwi_tif = rasterio.open(os.path.join(r'data\ndwi.tiff'), 'w', driver='Gtiff',
                             width=band_green.width, height=band_green.height,
                             count=1,
                             crs=band_green.crs,
                             transform=band_green.transform,
                             dtype='float32')
    band_green = band_green.read(1).astype('float64')
    band_nir = band_nir.read(1).astype('float64')
    ndwi = (band_green - band_nir) / (band_green + band_nir)
    ndwi_tif.write(ndwi, 1)
    ndwi_tif.close()

def get_path_to_image(in_dir):
    image_dir = os.path.join(in_dir, 'GRANULE')
    tree = os.walk(image_dir)
    image_dir = list(filter(lambda x: 'IMG_DATA' in x[0],list(tree)))
    match len(image_dir):
        case 1:
            bands_dir = [os.path.join(image_dir[0][0], i) for i in image_dir[0][2]]
    return bands_dir


def get_rgb(in_dir, out_dir):
    # red = rasterio.open(red_path)
    # green = rasterio.open(green_path)
    # blue = rasterio.open(blue_path)
    # rgb_tif = rasterio.open(os.path.join(r'data\rgb.tiff'), 'w', driver='Gtiff',
    #                         width=green.width, height=green.height,
    #                         count=3,
    #                         crs=green.crs,
    #                         transform=green.transform,
    #                         dtype='float32')
    #
    # red = normalize(brighten(red.read(1).astype('float32')))
    # green = normalize(brighten(green.read(1).astype('float32')))
    # blue = normalize(brighten(blue.read(1).astype('float32')))
    # rgb_tif.write(red, 1)
    # rgb_tif.write(green, 2)
    # rgb_tif.write(blue, 3)
    # rgb_tif.close()
    pass

def get_image_patches(data_dir):
    pass

if __name__ == "__main__":
    test_dir1 = r'C:\Users\SCII5\PycharmProjects\pythonProject\data\S2B_MSIL1C_20231019T062859_N0509_R077_T43UCB_20231019T081708.SAFE'
    test_dir2 = r'C:\Users\SCII5\PycharmProjects\pythonProject\data\S2B_MSIL2A_20231019T062859_N0509_R077_T43VCC_20231019T090833.SAFE'
    for i in get_path_to_image(test_dir1):
        print(i)




















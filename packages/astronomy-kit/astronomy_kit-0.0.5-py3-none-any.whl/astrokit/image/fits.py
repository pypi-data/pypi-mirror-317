import pathlib
import matplotlib.pyplot as plt
import numpy as np
from .noise import add_dot_source
from astropy.io import fits
from astropy.wcs import WCS
from tifffile import tifffile
from PIL import Image as PILImage
from pathlib import Path

from astrokit.utils import normalize


class Image(object):
    shape = None
    suffix = '.fits'
    header = None
    data = None

    def __init__(self, file: str | Path = None, data=None, header: dict | fits.Header = None, **kwargs):
        self.dtype = kwargs.get('dtype', np.float32)
        self.file = file
        self.data = data

        if file is not None:
            self.__init_form_file()
        elif data is not None:
            self.__init_form_data()
        else:
            raise ValueError('file or data must be provided')
        if self.header is not None:
            self.init_fits_header(header)

    def __init_form_file(self):
        self.suffix = self.file.suffix
        match self.suffix:
            case '.fits':
                self.load_image_from_fits()
            case '.tiff', '.tif':
                self.load_image_from_tiff()
            case '.npy':
                self.load_image_from_npy()
            case _:
                self.load_image()

    def __init_form_data(self):
        self.set_data(self.data)

    def load_image_from_fits(self):
        hdu = fits.open(self.file)
        data = hdu[0].data
        data = np.array(data, dtype=self.dtype)
        self.set_data(data)
        self.header = hdu[0].header
        hdu.close()

    def load_image_from_tiff(self):
        data = tifffile.imread(self.file)
        data = np.array(data, dtype=self.dtype)
        data = np.flipud(data)
        self.set_data(data)

    def load_image_from_npy(self):
        data = np.load(self.file)
        data = np.array(data, dtype=self.dtype)
        data = np.flipud(data)
        self.set_data(data)

    def load_image(self):
        with PILImage.open(self.file) as data:
            data = np.flipud(data)
            self.data = np.array(data, dtype=self.dtype)

    def init_fits_header(self, header):
        if isinstance(header, dict):
            header = fits.Header(header)
        elif header is None:
            header = dict()
            header['WCSAXES'] = len(self.shape)
            header['CTYPE1'] = 'RA---SIN'
            header['CTYPE2'] = 'DEC--SIN'
            header['CRPIX1'] = np.floor(self.shape[0] / 2 + 1)
            header['CRPIX2'] = np.floor(self.shape[0] / 2 + 1)
            header['CRVAL1'] = 15.0
            header['CRVAL2'] = -45.0
            header['CDELT1'] = -0.054539420584031
            header['CDELT2'] = 0.054539420584031
            header['CUNIT1'] = 'deg'
            header['CUNIT2'] = 'deg'
            header = fits.Header(header)

        self.header = header

    def set_header(self, header):
        self.init_fits_header(header)

    def show(self, **kwargs):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection=kwargs.get('wcs', None))
        im = ax.imshow(np.squeeze(self.data),
                       cmap=kwargs.get('cmap', 'viridis'),
                       origin='lower',
                       )
        ax.set_title(kwargs.get('title', str(self.file)))
        if kwargs.get('color_bar', True):
            fig.colorbar(im)
        if kwargs.get('show', True):
            fig.show()
        if kwargs.get('save_name', None) is not None:
            save_list = kwargs.get('save_name')
            if type(save_list) is not list:
                save_list = [save_list]
            for save_name in save_list:
                fig.savefig(save_name, dpi=kwargs.get('dpi', 100))

    def show_fits(self, **kwargs):
        self.show(wcs=WCS(self.header).sub(2), **kwargs)

    def get_data(self):
        return np.squeeze(self.data)

    def set_data(self, data):
        self.data = data
        self.shape = data.shape

    def save(self, filename: str | pathlib.Path):
        if type(filename) is str:
            filename = pathlib.Path(filename)
        suffix = filename.suffix
        data = np.flipud(self.get_data())
        match suffix:
            case '.fits':
                hdu = fits.PrimaryHDU(self.data, header=self.header)
                hdu.writeto(filename, overwrite=True)
            case '.tiff' | '.tif':
                tifffile.imwrite(filename, data, shape=data.shape)
            case '.npy':
                np.save(filename, data)
            case _:
                img = normalize(data) * 255
                img = PILImage.fromarray(img.astype(np.uint8), mode='L')
                img.save(filename)

    def add_noise(self, noise_type='dot-source', **kwargs):
        if noise_type == 'dot-source':
            self.add_dot_source(**kwargs)

    def add_dot_source(self, num=1, seed=None, sigma=1, x=None, y=None, power=1):
        """
        Add a dot source to the image.
        :param num: number of dot source
        :param seed: rand seed
        :param sigma: gaussian sigma size
        :param x: dot source x position
        :param y: dot source y position
        :param power: dot source power
        :return: image data after adding dot source
        """
        data = self.get_data()
        data = add_dot_source(data, num, seed, sigma, x, y, power)
        for _ in range(len(self.shape) - len(data.shape)):
            data = data[np.newaxis, ...]
        self.set_data(data)

    def __copy__(self):
        return Image(data=self.data, header=self.header, dtype=self.dtype)

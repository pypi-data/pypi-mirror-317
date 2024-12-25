#!/usr/bin/env python3
#
# Copyright (c) 2017-2018 Weitian LI <weitian@aaronly.me>
# MIT License
#

"""
Convert a FITS image to OSKAR sky model for simulation usage.

NOTE
----
The OSKAR sky model consists of all the valid pixels (with absolute
values within the specified minimum and maximum thresholds) from
the given image (i.e., slice at a frequency channel), and fluxes
are given in unit [Jy], therefore, the input image should be converted
from brightness temperature [K] to unit [Jy/pixel].

References
----------
[1] GitHub: OxfordSKA/OSKAR
    https://github.com/OxfordSKA/OSKAR
[2] OSKAR - Sky Model
    http://www.oerc.ox.ac.uk/~ska/oskar2/OSKAR-Sky-Model.pdf
[3] OSKAR - Settings
    http://www.oerc.ox.ac.uk/~ska/oskar2/OSKAR-Settings.pdf
"""

import os
import sys
import argparse
import logging
from datetime import datetime

import numpy as np
import astropy.io.fits as fits
import astropy.units as au
from astropy.wcs import WCS


logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s:%(lineno)d] %(message)s")
logger = logging.getLogger()


class SkyModel:
    """
    OSKAR sky model.

    Parameters
    ----------
    image : 2D float `~numpy.ndarray`
        Input image array; unit [K] (brightness temperature)
    freq : float
        Frequency of the input image slice; unit [MHz]
    pixelsize : float
        Pixel size of the input image;
        Unit: [arcsec]
    ra0, dec0 : float
        The coordinate of the image center; unit [deg]
    minvalue : float, optional
        The minimum threshold for the image absolute values
    maxvalue : float, optional
        The maximum threshold for the image absolute values
    mask : 2D bool `~numpy.ndarray`, optional
        Use this mask to select the sources of the output sky model,
        instead of the above ``minvalue`` and ``maxvalue``.
        NOTE: Will overwrite the above ``minvalue`` and ``maxvalue``.
    projection : str, optional
        The WCS projection for the image;
        Default: "CAR" (Cartesian)
        TODO: support "SIN" etc.
    """
    def __init__(self, image, freq, pixelsize, ra0, dec0,
                 minvalue=1e-4, maxvalue=np.inf, mask=None,
                 projection="CAR"):
        self.image = image  # [K] (brightness temperature)
        self.freq = freq  # [MHz]
        self.pixelsize = pixelsize  # [arcsec]
        self.ra0 = ra0  # [deg]
        self.dec0 = dec0  # [deg]
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.mask = mask
        self.projection = projection
        logger.info("SkyModel: Loaded image @ %.2f [MHz], " % freq +
                    "%.1f [arcsec/pixel]" % pixelsize)
        logger.info("Image size: %dx%d" % self.shape)
        logger.info("FoV size: %.2fx%.2f [deg^2]" % self.fov)

    @property
    def shape(self):
        """
        FITS image (width, height)
        """
        width, height = list(reversed(self.image.shape))[:2]
        return (width, height)

    @property
    def fov(self):
        """
        FITS image FoV size: (width, height) [deg]
        """
        width, height = self.shape
        return (width*self.pixelsize/3600, height*self.pixelsize/3600)

    @property
    def wcs(self):
        """
        WCS for the given image slice.
        """
        shape = self.image.shape
        delta = self.pixelsize / 3600.0  # [arcsec] -> [deg]
        wcs_ = WCS(naxis=2)
        wcs_.wcs.ctype = ["RA---"+self.projection, "DEC--"+self.projection]
        wcs_.wcs.crval = np.array([self.ra0, self.dec0])
        wcs_.wcs.crpix = np.array([shape[1], shape[0]]) / 2.0 + 1
        wcs_.wcs.cdelt = np.array([-delta, delta])  # NOTE the minus sign
        return wcs_

    @property
    def fits_header(self):
        header = self.wcs.to_header()
        header["BUNIT"] = ("Jy/pixel", "Brightness unit")
        header["FREQ"] = (self.freq, "Frequency [MHz]")
        header["RA0"] = (self.ra0, "Center R.A. [deg]")
        header["DEC0"] = (self.dec0, "Center Dec. [deg]")
        header["PixSize"] = (self.pixelsize, "Pixel size [arcsec]")
        header["K2JyPix"] = (self.factor_K2JyPixel, "[K] -> [Jy/pixel]")
        header["MINVALUE"] = (self.minvalue, "[K] minimum threshold")
        if np.isfinite(self.maxvalue):
            header["MAXVALUE"] = (self.maxvalue, "[K] maximum threshold")
        return header

    @property
    def factor_K2JyPixel(self):
        """
        Conversion factor from [K] to [Jy/pixel]
        """
        pixarea = (self.pixelsize * au.arcsec) ** 2
        freq = self.freq * au.MHz
        # astro 2.0x slower than the following
        # equiv = au.brightness_temperature(pixarea, freq)
        # new version of astropy (3.0.1) has a bug in the above
        equiv = au.brightness_temperature(freq, pixarea)
        factor = au.K.to(au.Jy, equivalencies=equiv)
        return factor

    @property
    def ra_dec(self):
        """
        Calculate the (ra, dec) of each image pixel using the above WCS.

        NOTE: axis ordering difference between numpy array and FITS
        """
        shape = self.image.shape
        wcs = self.wcs
        x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
        pix = np.column_stack([x.flatten(), y.flatten()])
        world = wcs.wcs_pix2world(pix, 0)
        ra = world[:, 0].reshape(shape)
        dec = world[:, 1].reshape(shape)
        return (ra, dec)

    @property
    def mask(self):
        if self._mask is None:
            self._mask = ((np.abs(self.image) >= self.minvalue) &
                          (np.abs(self.image) <= self.maxvalue))
            logger.info("Use minimum and maximum thresholds: [%.4e, %.4e]" %
                        (self.minvalue, self.maxvalue))
        return self._mask

    @mask.setter
    def mask(self, value):
        if (value is not None) and (value.shape != self.image.shape):
            raise ValueError("mask shape does match image!")
        self._mask = value

    @property
    def sky(self):
        """
        OSKAR sky model array converted from the input image.

        Columns
        -------
        ra : (J2000) right ascension (deg)
        dec : (J2000) declination (deg)
        flux : source (Stokes I) flux density (Jy)
        """
        idx = self.mask.flatten()
        ra, dec = self.ra_dec
        ra = ra.flatten()[idx]
        dec = dec.flatten()[idx]
        flux = self.image.flatten()[idx] * self.factor_K2JyPixel
        sky_ = np.column_stack([ra, dec, flux])
        return sky_

    def write_sky_model(self, outfile, clobber=False):
        """
        Write the converted sky model for simulation.
        """
        if os.path.exists(outfile) and (not clobber):
            raise OSError("OSKAR sky model file already exists: %s" % outfile)
        sky = self.sky
        counts = sky.shape[0]
        percent = 100 * counts / self.image.size
        logger.info("Source counts: %d (%.1f%%)" % (counts, percent))
        header = ("Frequency = %.3f [MHz]\n" % self.freq +
                  "Pixel size = %.2f [arcsec]\n" % self.pixelsize +
                  "K2JyPixel = %.3e\n" % self.factor_K2JyPixel +
                  "RA0 = %.4f [deg]\n" % self.ra0 +
                  "Dec0 = %.4f [deg]\n" % self.dec0 +
                  "Minimum value = %.4e [K]\n" % self.minvalue +
                  "Maximum value = %.4e [K]\n" % self.maxvalue +
                  "Source counts = %d (%.1f%%)\n\n" % (counts, percent) +
                  "R.A.[deg]    Dec.[deg]    flux[Jy]")
        logger.info("Writing sky model ...")
        np.savetxt(outfile, sky, fmt='%.10e, %.10e, %.10e', header=header)
        logger.info("Wrote OSKAR sky model to file: %s" % outfile)

    def write_fits(self, outfile, oldheader=None, clobber=False):
        if os.path.exists(outfile) and (not clobber):
            raise OSError("Sky FITS already exists: %s" % outfile)
        if oldheader is not None:
            header = oldheader
            header.extend(self.fits_header, update=True)
        else:
            header = self.fits_header
        header.add_history(datetime.now().isoformat())
        header.add_history(" ".join(sys.argv))
        image = self.image.copy()
        image[~self.mask] = np.nan
        image *= self.factor_K2JyPixel
        hdu = fits.PrimaryHDU(data=image, header=header)
        try:
            hdu.writeto(outfile, overwrite=True)
        except TypeError:
            hdu.writeto(outfile, clobber=True)  # old astropy versions
        logger.info("Wrote FITS image of sky model to file: %s" % outfile)

    def write_mask(self, outfile, clobber=False):
        if os.path.exists(outfile) and (not clobber):
            raise OSError("Sky mask already exists: %s" % outfile)
        header = self.fits_header
        header.add_history(datetime.now().isoformat())
        header.add_history(" ".join(sys.argv))
        hdu = fits.PrimaryHDU(data=self.mask.astype(np.int16),
                              header=header)
        try:
            hdu.writeto(outfile, overwrite=True)
        except TypeError:
            hdu.writeto(outfile, clobber=True)  # old astropy versions
        logger.info("Wrote mask of sky model to file: %s" % outfile)


def main():
    parser = argparse.ArgumentParser(
        description="Convert FITS image to OSKAR sky model")
    parser.add_argument("-C", "--clobber", dest="clobber",
                        action="store_true",
                        help="overwrite existing file")
    parser.add_argument("-r", "--ra0", dest="ra0", type=float,
                        default=0.0,
                        help="[deg] R.A. of the image center (default: 0)")
    parser.add_argument("-d", "--dec0", dest="dec0", type=float,
                        default=-27.0,
                        help="[deg] Dec. of the image center (default: -27)")
    parser.add_argument("-p", "--pixel-size", dest="pixelsize", type=float,
                        help="image pixel size [arcsec]; " +
                        "(default: obtain from the FITS header 'PixSize')")
    parser.add_argument("-f", "--freq", dest="freq", type=float,
                        help="frequency [MHz] the image measured; " +
                        "(default: obtain from the FITS header 'FREQ')")
    parser.add_argument("-m", "--min-value", dest="minvalue",
                        type=float, default=1e-4,
                        help="[K] minimum threshold to the output sky model " +
                        "(default: 1e-4, i.e., 0.1 mK)")
    parser.add_argument("-M", "--max-value", dest="maxvalue",
                        type=float, default=np.inf,
                        help="[K] maximum threshold to the output sky model " +
                        "(default: inf)")
    parser.add_argument("--mask", dest="mask",
                        help="use a mask to determine the output sky model " +
                        "(NOTE: will override --min-value and --max-value)")
    parser.add_argument("-F", "--osm-fits", dest="osmfits",
                        action="store_true",
                        help="save a FITS version of the converted sky model")
    parser.add_argument("-o", "--outdir", dest="outdir",
                        help="output directory for sky model files " +
                        "(default: current working directory)")
    parser.add_argument("--create-mask", dest="create_mask",
                        help="create a FITS mask for the output sky model")
    parser.add_argument("infile", help="input FITS image")
    parser.add_argument("outfile", nargs="?",
                        help="output OSKAR sky model (default: " +
                        "same basename as the input FITS image)")
    args = parser.parse_args()

    if args.outfile:
        outfile = args.outfile
    else:
        outfile = os.path.splitext(os.path.basename(args.infile))[0] + ".osm"
        if args.outdir:
            outfile = os.path.join(args.outdir, outfile)
            if not os.path.exists(args.outdir):
                os.mkdir(args.outdir)

    with fits.open(args.infile) as f:
        image = f[0].data.astype(np.float32)
        header = f[0].header.copy(strip=True)
    logger.info("Read input FITS image: %s" % args.infile)

    # Check data unit
    unit = header.get("BUNIT")
    if unit is None:
        logger.warning("Input FITS file of unknown data unit! " +
                       "Assuming [K] (kelvin)!")
    elif unit.upper() not in ["K", "KELVIN"]:
        logger.error("Input FITS file of wrong data unit: %s" % unit)

    freq = args.freq if args.freq else header["FREQ"]  # [MHz]
    if args.pixelsize:
        pixelsize = args.pixelsize  # [arcsec]
    else:
        pixelsize = header["PixSize"]  # [arcsec]
    logger.info("Frequency: %.2f [MHz]" % freq)
    logger.info("Pixel size: %.2f [arcsec]" % pixelsize)
    if args.mask:
        mask = fits.open(args.mask)[0].data.astype(np.bool)
        logger.info("Loaded sky mask from file: %s" % args.mask)
    else:
        mask = None
        logger.info("Threshold: %g - %g [K]" % (args.minvalue, args.maxvalue))
    skymodel = SkyModel(image=image, freq=freq, ra0=args.ra0, dec0=args.dec0,
                        pixelsize=pixelsize, minvalue=args.minvalue,
                        maxvalue=args.maxvalue, mask=mask)
    logger.info("Conversion [K] -> [Jy/pixel]: %g" % skymodel.factor_K2JyPixel)
    skymodel.write_sky_model(outfile, clobber=args.clobber)
    if args.osmfits:
        outfits = outfile + ".fits"
        skymodel.write_fits(outfits, oldheader=header, clobber=args.clobber)
    if args.create_mask:
        skymodel.write_mask(args.create_mask, clobber=args.clobber)


if __name__ == "__main__":
    main()

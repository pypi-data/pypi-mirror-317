from __future__ import division

import scipy.special as sp
import numpy as np
from skimage.transform import resize


def Sersic2D(x, y, mag=12.0, r_eff=1.0, n=2.0, ellip=0.5,
             theta=0.0, x_0=0.0, y_0=0.0, pixelscale=0.01):
    """
    Sersic2D: Caculate the surface brightness at given spatial position
     base on the Sersic model.

    Parameters
    ----------
    x : float array
        Coordinate of spatial position in the x-axis
    y : float array
        Coordinate of spatial position in the y-axis
    mag : float, optional
        Integral magnitude of sersic model, by default 12.0
    r_eff : float, optional
        Effective radius in pixel, by default 1.0
    n : float, optional
        Sersic index, by default 2.0
    ellip : float, optional
        Ellipticity, by default 0.5
    theta : float, optional
        Position angle in degree, by default 0.0
    x_0 : float, optional
        Offset of the center of Sersic model in x-axis, by default 0.0
    y_0 : float, optional
        Offset of the center of Sersic model in y-axis, by default 0.0
    pixelscale : float, optional
        Size of each pixel in arcsec^2, by default 0.01

    Returns
    -------
        _description_
    """

    # Convert the angle in degree to angle to radians
    theta_radian = theta / 180 * np.pi

    # Produce Sersic profile
    bn = sp.gammaincinv(2. * n, 0.5)
    a, b = r_eff, (1 - ellip) * r_eff
    cos_theta, sin_theta = np.cos(theta_radian), np.sin(theta_radian)
    x_maj = (x - x_0) * cos_theta + (y - y_0) * sin_theta
    x_min = -(x - x_0) * sin_theta + (y - y_0) * cos_theta
    z = (abs(x_maj / a) ** 2 + abs(x_min / b) ** 2) ** (1 / 2)
    profile = np.exp(-bn * (z ** (1 / n) - 1))

    # Normalization
    integral = a * b * 2 * np.pi * n * np.exp(bn) / (bn ** (2 * n)) * sp.gamma(2 * n)
    prof_norm = profile / integral * pixelscale

    # Calibration
    total_flux = 10. ** ((22.5 - mag) * 0.4)
    sb_mag = 22.5 - 2.5 * np.log10(prof_norm * total_flux / pixelscale)

    return sb_mag


def VelMap2D(x, y, vmax=200.0, rt=1.0, ellip=0.5,
             theta=0.0, x_0=0.0, y_0=0.0):
    """
    VelMap2D: Caculate the velocity at given spatial position base on the rotating disk model.
    The rotation curve is adpot as the tanh model.

    Parameters
    ----------
    x : float array
        Coordinate of spatial position in the x-axis
    y : float array
        Coordinate of spatial position in the y-axis
    vmax : float, optional
        Maximum rotational velocity of rotation curve, by default 200.0
    rt : float, optional
        Turn-over radius of rotation curve, by default 1.0
    ellip : float, optional
        Ellipicity of disk model, by default 0.5
    theta : float, optional
        Position angle of disk model, by default 0.0
    x_0 : float, optional
        Offset of the center of disk model in the x-axis, by default 0.0
    y_0 : float, optional
        Offset of the center of disk model in the y-axis, by default 0.0

    Returns
    -------
    _type_
        _description_
    """

    # Convert the angle in degree to angle to radians
    theta_radian = theta / 180 * np.pi

    # Produce tanh profile
    a, b = rt, (1 - ellip) * rt
    cos_theta, sin_theta = np.cos(theta_radian), np.sin(theta_radian)
    x_maj = (x - x_0) * cos_theta + (y - y_0) * sin_theta
    x_min = -(x - x_0) * sin_theta + (y - y_0) * cos_theta
    z = (abs(x_maj / a) ** 2 + abs(x_min / b) ** 2) ** (1 / 2)
    profile = vmax * np.tanh(z) * ((x_maj / a) / z)

    return profile


def GradMap2D(x, y, a0=10.0, r_eff=1.0, gred=-1.0, ellip=0.5,
              theta=0.0, x_0=0.0, y_0=0.0):
    """
    GradMap2D: Caculate the intensity at given spatial position base on the disk model.
    The radial profile is adpot as the gradient model.

    Parameters
    ----------
    x : float array
        Coordinate of spatial position in the x-axis
    y : float array
        Coordinate of spatial position in the y-axis
    a0 : float, optional
        Intensity at the center, by default 10.0
    r_eff : float, optional
        Effective radius, by default 1.0
    gred : float, optional
        Gradient, by default -1.0
    ellip : float, optional
        Ellipicity of disk model, by default 0.5
    theta : float, optional
        Position angle of disk model, by default 0.0
    x_0 : float, optional
        Offset of the center of disk model in the x-axis, by default 0.0
    y_0 : float, optional
        Offset of the center of disk model in the y-axis, by default 0.0

    Returns
    -------
    _type_
        _description_
    """

    # Convert the angle in degree to angle to radians
    theta_radian = theta / 180 * np.pi

    # Produce gradiant profile
    a, b = r_eff, (1 - ellip) * r_eff
    cos_theta, sin_theta = np.cos(theta_radian), np.sin(theta_radian)
    x_maj = (x - x_0) * cos_theta + (y - y_0) * sin_theta
    x_min = -(x - x_0) * sin_theta + (y - y_0) * cos_theta
    z = (abs(x_maj / a) ** 2 + abs(x_min / b) ** 2) ** (1 / 2)
    profile = a0 + z * gred

    return profile


class Map2d(object):

    def __init__(self, config):
        """
        __init__ _summary_

        Parameters
        ----------
        inst : _type_
            _description_
        """
        self.xsamp = config.dpix
        self.ysamp = config.dpix
        startx = -(config.nx - 1) / 2.0 * self.xsamp
        stopx = (config.nx - 1) / 2.0 * self.xsamp
        starty = -(config.ny - 1) / 2.0 * self.ysamp
        stopy = (config.ny - 1) / 2.0 * self.ysamp
        xvals = np.linspace(startx, stopx, num=config.nx)
        yvals = np.linspace(starty, stopy, num=config.ny)

        ones = np.ones((config.ny, config.nx))
        x = ones * xvals
        y = np.flipud(ones * yvals.reshape(int(config.ny), 1))

        self.nx = config.nx
        self.ny = config.ny
        self.x = x
        self.y = y
        self.row = xvals
        # flip Y axis because we use Y increasing from bottom to top
        self.col = yvals[::-1]

    def shift_rotate(self, yoff, xoff, rot):
        """
        Return shifted/rotated (y, x) given offsets (yoff, xoff) and rotation, rot (degrees)

        Parameters
        ----------
        yoff, xoff: float
            yoff, xoff offsets in world coordinates
        rot: float
            rotation angle in degrees

        Returns
        -------
        ysh_rot, xsh_rot: 2D numpy arrays
            rotated and shifted copies of Grid.x and Grid.y
        """
        pa_radians = np.pi * rot / 180.0
        xsh = self.x - xoff
        ysh = self.y - yoff
        xsh_rot = xsh * np.cos(pa_radians) + ysh * np.sin(pa_radians)
        ysh_rot = -xsh * np.sin(pa_radians) + ysh * np.cos(pa_radians)
        return ysh_rot, xsh_rot

    def sersic_map(self, mag=12.0, r_eff=2.0, n=2.5, ellip=0.5, theta=-50.0):
        """
        Generate 2D map of Sersic model

        Parameters
        ----------
        mag : float, optional
            Integral magnitude, by default 12.0
        reff : float, optional
            Effective radius in arcsec, by default 2.0
        n : float, optional
            Sersic index, by default 2.5
        ellip : float, optional
            Ellipcity, by default 0.5
        theta : float, optional
            Position angle in degree, by default -50.0
        """

        # Check Input Parameters
        if (mag > 26) or (mag < 8):
            print("Notice: Your input integral magnitude of Sersic mode (mag) is > 26 mag or < 8 mag.")
        if (r_eff < 0):
            raise Exception("Effective radius (r_eff) should be > 0 arcsec!")
            # print("Effective radius (r_eff) should be > 0 arcsec!")
        if (n < 0):
            raise Exception("Sersic index (n) should be > 0!")
        if (ellip > 1) or (ellip < 0):
            raise Exception("Ellipcity (ellip) should be >= 0 and < 1!")
        if (ellip == 0):
            print("Notice: Ellipcity (ellip) should be >= 0 and < 1!")
        if (theta > 180) or (theta < -180):
            print("Notice: Your input position angle (theta) is > 180 degree or < -180 degree.")

        self.reff = r_eff / self.xsamp
        self.mag = mag
        self.n = n
        self.ellip = ellip
        self.theta = theta
        self.map = Sersic2D(self.x, self.y, mag=self.mag,
                            r_eff=self.reff, n=self.n,
                            ellip=self.ellip, theta=self.theta,
                            pixelscale=self.xsamp * self.ysamp)

    def tanh_map(self, vmax=200.0, rt=2.0, ellip=0.5, theta=-50.0):
        """
        Generate 2D velocity map of rotating disk according to tanh rotation curve

        Parameters
        ----------
        vmax : float, optional
            Maximum rotational velocity, by default 200.0km/s
        rt : float, optional
            Turn-over radius of rotation curve, by default 2.0 arcsec
        ellip : float, optional
            Apparent ellipcity of rotating disk, by default 0.5
        theta : float, optional
            Position angle of rotating disk, by default -50.0
        """

        # Check Input Parameters
        if (vmax <= 0):
            # print("Notice: Your input maximum rotational velocity (vmax) is <= 0 km/s!")
            raise Exception("Maximum rotational velocity (vmax) should be >0 km/s!")
        if (rt <= 0):
            # raise Exception("Turn-over radius (rt) should be > 0 arcsec!")
            raise Exception("Turn-over radius (rt) should be > 0 arcsec!")
        if (ellip > 1) or (ellip < 0):
            raise Exception("Ellipcity (ellip) should be >= 0 and < 1!")
            # print("Ellipcity (ellip) should be >= 0 and < 1!")
        if (theta > 180) or (theta < -180):
            print("Notice: Your input position angle (theta) is > 180 degree or < -180 degree.")

        self.vmax = vmax
        self.rt = rt / self.xsamp
        self.ellip = ellip
        self.theta = theta
        self.map = VelMap2D(self.x, self.y, vmax=self.vmax, rt=self.rt,
                            ellip=self.ellip, theta=self.theta)

    def gred_map(self, a0=10, r_eff=1, gred=-1, ellip=0.5, theta=0):
        """
        Generate 2D maps according to the radial gradient form

        Parameters
        ----------
        a0 : float, optional
            Amplitude at the center, by default 10
        r_eff : float, optional
            Effective radius, by default 1
        gred : float, optional
            Gradient of radial profile, by default -1
        ellip : float, optional
            Ellipcity, by default 0.5
        theta : int, optional
            Position angle, by default 0
        """
        # Check Input Parameters
        if (r_eff <= 0):
            raise Exception("Effective radius (r_eff) should be > 0 arcsec!")
            # print("Effective radius (r_eff) should be > 0 arcsec!")
        if (ellip > 1) or (ellip < 0):
            # raise Exception("Ellipcity (ellip) should be >= 0 and < 1!")
            print("Notice: Ellipcity (ellip) should be >= 0 and < 1!")
        if (theta > 180) or (theta < -180):
            print("Notice: Your input position angle (theta) is > 180 degree or < -180 degree.")

        self.a0 = a0
        self.reff = r_eff / self.xsamp
        self.gred = gred
        self.ellip = ellip
        self.theta = theta
        self.map = GradMap2D(self.x, self.y, a0=self.a0, r_eff=self.reff,
                             gred=self.gred, ellip=self.ellip, theta=self.theta)

    def load_map(self, image):
        """
        Generate 2D map according to input image

        Parameters
        ----------
        image : 2d numpy array
            The 2d array to be loaded.
        """
        if np.ndim(image) == 2:
            self.map = resize(image, (self.nx, self.ny))
        else:
            raise Exception("Input array should be a 2d-array!")


class StellarPopulationMap():
    """
    Class of 2D maps for the parameters of stellar population, such as
    surface brightness, median age and metallicity of stellar population,
    velocity and velocity dispersion maps, and dust extinction.

    Parameters
    ----------
    config : class
        Class of configuration
    sbright : class, optional
        Class of the map of surface brightness of stellar population, by default None
    logage : class, optional
        Class of the map of stellar age, by default None
    feh : class, optional
        Class of the map of stellar metellicity, by default None
    vel : class, optional
        Class of the map of stellar velocity, by default None
    vdisp : class, optional
        Class of the map of stellar velocity dispersion, by default None
    ebv : class, optional
        Class of the map of dust extinction, by default None
    """
    def __init__(self, config, sbright=None, logage=None,
                 feh=None, vel=None, vdisp=None, ebv=None):

        self.nx = config.nx
        self.ny = config.ny
        self.dpix = config.dpix
        self.fov_x = config.fov_x
        self.fov_y = config.fov_y

        if (sbright is None):
            print('Input SurfaceBrightness Map is empty!')
        else:
            self.sbright = sbright.map
            self.mag = self.sbright - 2.5 * np.log10(self.dpix * self.dpix)

        if (logage is None):
            print('Input Age Map is empty!')
        else:
            self.logage = logage.map
            self.age = 10 ** self.logage / 1e9

        if (feh is None):
            print('Input Metallicity Map is empty!')
        else:
            self.feh = feh.map

        if (vel is None):
            print('Input Velocity Map is empty!')
        else:
            self.vel = vel.map

        if (vdisp is None):
            print('Input VelocityDispersion Map is empty!')
        else:
            self.vdisp = vdisp.map
            ind_overrange = (self.vdisp < 10)
            if len(self.vdisp[ind_overrange]) > 0:
                print("Notice: Spaxel with <10km/s in the input vdisp map will be automatically adjusted to 10km/s.")
            self.vdisp[ind_overrange] = 10

        if (ebv is None):
            print('Input EBV Map is empty!')
        else:
            self.ebv = ebv.map
            ind_overrange = (self.ebv < 0)
            if len(self.ebv[ind_overrange]) > 0:
                print("Notice: Spaxel with < 0 mag in the input ebv map will be automatically adjusted to 0 mag.")
            self.ebv[ind_overrange] = 0


class IonizedGasMap():
    """
    Class of 2D maps for the parameters of ionized gas, such as
    Halpha flux map, gas-phase metallicity map,
    velocity and velocity dispersion maps, and dust extinction.

    Parameters
    ----------
    config : class
        Class of configuration
    halpha : class, optional
        Class of the map of Halpha flux, by default None
    zh : class, optional
        Class of the map of gas-phase metallicity, by default None
    vel : class, optional
        Class of the map of gas velocity, by default None
    vdisp : class, optional
        Class of the map of gas velocity dispersion, by default None
    ebv : class, optional
        Class of the map of dust extinction, by default None
    """
    def __init__(self, config, halpha=None, zh=None, vel=None, vdisp=None, ebv=None):

        self.nx = config.nx
        self.ny = config.ny
        self.dpix = config.dpix
        self.fov_x = config.fov_x
        self.fov_y = config.fov_y

        if (halpha is None):
            print('Input Halpha Map is empty!')
        else:
            self.halpha = halpha.map

        if (zh is None):
            print('Input ZH Map is empty!')
        else:
            self.zh = zh.map

        if (vel is None):
            print('Input Vel Map is empty!')
        else:
            self.vel = vel.map

        if (vdisp is None):
            print('Input Vdisp Map is empty!')
        else:
            self.vdisp = vdisp.map
            # Fix the spaxels whose vdisp is too small
            ind_overrange = (self.vdisp < 10)
            if len(self.vdisp[ind_overrange]) > 0:
                print("Notice: Spaxel with <10km/s in the input vdisp map will be automatically adjusted to 10km/s.")
            self.vdisp[ind_overrange] = 10

        if (ebv is None):
            print('Input EBV Map is empty!')
        else:
            self.ebv = ebv.map
            # Fix the spaxels whose ebv is negtive
            ind_overrange = (self.ebv < 0)
            if len(self.ebv[ind_overrange]) > 0:
                print("Notice: Spaxel with < 0 mag in the input ebv map will be automatically adjusted to 0 mag.")
            self.ebv[ind_overrange] = 0

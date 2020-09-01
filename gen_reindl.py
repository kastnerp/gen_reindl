import math


class GenReindl:
    """
    Python port of 'gen_reindl.exe', a program that transforms global irradiances into orizontal diffuse and direct normal irradiances.

    ...


    Methods
    -------
    calc_split(month, day, time, irrad_glo)
        Calculates a tuple of direct normal irradiation and diffuse horizontal irradiation
    """

    def __init__(self, lat, lon, time_zone):

        """
        Parameters
        ----------
        lat  : float
            latitude (north positive)
        lon : float
            longitude (west positive)
        time_zone  : int
            Time zone in a multiple of 15 degrees from the meridian. Example: for Singapore, UTC+8 * 15 = -120, despite a -103.98 longitude.
        """

        self.solar_constant_e = 1367.0
        self.DTR = 0.017453292  # Pi / 180
        self.RTD = 57.2957795  # 180 / Pi
        self.lat = lat
        self.lon = lon
        self.time_zone = time_zone

        self.time = None
        self.month = None
        self.day = None
        self.irrad_beam_nor = None
        self.irrad_dif = None

    def month_and_day_to_julian_day(self, month, day):
        if month == 1:
            return day
        if month == 2:
            return day + 31
        if month == 3:
            return day + 59
        if month == 4:
            return day + 90
        if month == 5:
            return day + 120
        if month == 6:
            return day + 151
        if month == 7:
            return day + 181
        if month == 8:
            return day + 212
        if month == 9:
            return day + 243
        if month == 10:
            return day + 273
        if month == 11:
            return day + 304
        if month == 12:
            return day + 334
        else:
            print("bad month")

    def solar_elev_azi_ecc(self, latitude,
                           longitude,
                           time_zone,
                           jday,
                           time,
                           solar_time=0):
        # /*  angles in degrees, times in hours  */

        # /*  solar elevation and azimuth formulae from sun.c  */
        if solar_time == 1:
            sol_time = time
        if solar_time == 0:
            sol_time = time + 0.170 * math.sin(
                (4 * math.pi / 373) * (jday - 80)) - 0.129 * math.sin(
                (2 * math.pi / 355) *
                (jday - 8)) + 12 / 180.0 * (time_zone - longitude)

        solar_declination = self.RTD * 0.4093 * math.sin(
            (2 * math.pi / 368) * (jday - 81))
        jday_angle = 2 * math.pi * (jday - 1) / 365

        solar_elevation = self.RTD * math.asin(
            math.sin(latitude * self.DTR) * math.sin(solar_declination * self.DTR) -
            math.cos(latitude * self.DTR) * math.cos(solar_declination * self.DTR) *
            math.cos(sol_time * (math.pi / 12)))

        solar_azimuth = self.RTD * (-math.atan2(
            math.cos(solar_declination * self.DTR) * math.sin(sol_time *
                                                              (math.pi / 12)),
            -math.cos(latitude * self.DTR) * math.sin(solar_declination * self.DTR) -
            math.sin(latitude * self.DTR) * math.cos(solar_declination * self.DTR) *
            math.cos(sol_time * (math.pi / 12))))

        # /*  eccentricity_correction formula used in genjdaylit.c */

        eccentricity_correction = 1.00011 + 0.034221 * math.cos(
            jday_angle) + 0.00128 * math.sin(jday_angle) + 0.000719 * math.cos(
            2 * jday_angle) + 0.000077 * math.sin(2 * jday_angle)

        return solar_elevation, solar_azimuth, eccentricity_correction

    def diffuse_fraction(self, irrad_glo, solar_elevation, eccentricity_correction):
        dif_frac = 0

        if solar_elevation > 0:
            irrad_ex = self.solar_constant_e * eccentricity_correction * math.sin(
                self.DTR * solar_elevation)
        else:
            irrad_ex = 0

        if irrad_ex > 0:
            index_glo_ex = irrad_glo / irrad_ex
        else:
            return 0

        if index_glo_ex < 0:
            print("negative irrad_glo in diffuse_fraction_th\n")
        if index_glo_ex > 1:
            index_glo_ex = 1

        if index_glo_ex <= 0.3:
            dif_frac = 1.02 - 0.254 * index_glo_ex + 0.0123 * math.sin(
                self.DTR * solar_elevation)
        if dif_frac > 1:
            dif_frac = 1

        if 0.3 < index_glo_ex < 0.78:
            dif_frac = 1.4 - 1.749 * index_glo_ex + 0.177 * math.sin(self.DTR * solar_elevation)
        if dif_frac > 0.97:
            dif_frac = 0.97
        if dif_frac < 0.1:
            dif_frac = 0.1

        if index_glo_ex >= 0.78:
            dif_frac = 0.486 * index_glo_ex - 0.182 * math.sin(
                self.DTR * solar_elevation)
        if dif_frac < 0.1:
            dif_frac = 0.1

        return dif_frac

    def calc_split(self, month, day, time, irrad_glo):

        """Calculates a tuple of direct normal irradiation and diffuse horizontal irradiation

        Parameters
        ----------
        month : int
            month
        day : int
            day
        time : float
            hour of the day
        irrad_glo :
            Global irradiation from e.g. a weather station

        Returns
        -------
        tuple
            Direct normal irradiation and diffuse horizontal irradiation
        """

        jday = self.month_and_day_to_julian_day(month, day)

        if irrad_glo < 0 or irrad_glo > self.solar_constant_e:  # / * check irradiances and exit if necessary * /
            irrad_glo = self.solar_constant_e

        # no object orientation yet

        solar_elevation, solar_azimuth, eccentricity_correction = self.solar_elev_azi_ecc(
            self.lat, self.lon, self.time_zone, jday, time)

        #

        irrad_dif = self.diffuse_fraction(irrad_glo, solar_elevation,
                                          eccentricity_correction) * irrad_glo

        if solar_elevation > 5.0:

            irrad_beam_nor = (irrad_glo - irrad_dif) * 1.0 / math.sin(
                self.DTR * solar_elevation)

        else:
            irrad_beam_nor = 0
            irrad_dif = irrad_glo

        if irrad_beam_nor > self.solar_constant_e:
            irrad_beam_nor = self.solar_constant_e
            irrad_dif = irrad_glo - irrad_beam_nor * math.sin(
                self.DTR * solar_elevation)

        # print(month, day, round(time, 2), round(irrad_beam_nor, 2), round(irrad_dif, 2))

        self.time = time
        self.month = month
        self.day = day
        self.irrad_beam_nor = irrad_beam_nor
        self.irrad_dif = irrad_dif

        return irrad_beam_nor, irrad_dif

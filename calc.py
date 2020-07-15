# !pip install pvlib
import pvlib
# https://pvlib-python.readthedocs.io/en/stable/generated/pvlib.irradiance.reindl.html?highlight=reindl#pvlib.irradiance.reindl

# conda install -c pvlib pvlib
import pandas as pd
import math

# Create date series using date_range() function
date_series = pd.date_range('01/01/2019', periods=8760, freq='H')
# print(date_series)

# altitude GFR Station
altitude = 294

# lat, lon taken from GFR
lon = 42.449
lat = -76.449
lat = 76.449
time_zone = -5

pos = pvlib.solarposition.get_solarposition(date_series, lat, lon)
pos

# gen_reindl:
# Program that transforms global irradiances into orizontal diffuse and direct normal irradiances
# Note that the -o option has to be specified!
# Note that the -i option has to be specified!
#
# Supported options are:
# -i       input file [format: month day hour global_irradiation
# -o       output file [format: month day hour dir_norm_irrad dif_hor_irrad
# -m       time zone
# -l       longitude [DEG, West is positive]
# -a       latitude [DEG, North is positive]


solar_constant_e = 1367.0
DTR = 0.017453292  # Pi / 180
RTD = 57.2957795  # 180 / Pi


def month_and_day_to_julian_day(month, day):
    if (month == 1):  return day
    if (month == 2):  return day + 31
    if (month == 3):  return day + 59
    if (month == 4):  return day + 90
    if (month == 5):  return day + 120
    if (month == 6):  return day + 151
    if (month == 7):  return day + 181
    if (month == 8):  return day + 212
    if (month == 9):  return day + 243
    if (month == 10):  return day + 273
    if (month == 11):  return day + 304
    if (month == 12):
        return day + 334
    else:
        print("bad month")


def solar_elev_azi_ecc(latitude, longitude, time_zone, jday, time, solar_time=0):
    # /*  angles in degrees, times in hours  */

    # /*  solar elevation and azimuth formulae from sun.c  */
    if (solar_time == 1):   sol_time = time
    if (solar_time == 0):   sol_time = time + 0.170 * math.sin((4 * math.pi / 373) * (jday - 80)) - 0.129 * math.sin((2 * math.pi / 355) * (jday - 8)) + 12 / 180.0 * (
            time_zone - longitude)

    solar_declination = RTD * 0.4093 * math.sin((2 * math.pi / 368) * (jday - 81))
    jday_angle = 2 * math.pi * (jday - 1) / 365

    solar_elevation = RTD * math.asin(
        math.sin(latitude * DTR) * math.sin(solar_declination * DTR) - math.cos(latitude * DTR) * math.cos(solar_declination * DTR) * math.cos(sol_time * (math.pi / 12)))

    solar_azimuth = RTD * (-math.atan2(math.cos(solar_declination * DTR) * math.sin(sol_time * (math.pi / 12)),
                                       -math.cos(latitude * DTR) * math.sin(solar_declination * DTR) -
                                       math.sin(latitude * DTR) * math.cos(solar_declination * DTR) * math.cos(sol_time * (math.pi / 12))))

    # /*  eccentricity_correction formula used in genjdaylit.c */

    eccentricity_correction = 1.00011 + 0.034221 * math.cos(jday_angle) + 0.00128 * math.sin(jday_angle) + 0.000719 * math.cos(2 * jday_angle) + 0.000077 * math.sin(2 * jday_angle)

    return solar_elevation, solar_azimuth, eccentricity_correction


def diffuse_fraction(irrad_glo, solar_elevation, eccentricity_correction):
    dif_frac = 0

    if (solar_elevation > 0):
        irrad_ex = solar_constant_e * eccentricity_correction * math.sin(DTR * solar_elevation)
    else:
        irrad_ex = 0

    if (irrad_ex > 0):
        index_glo_ex = irrad_glo / irrad_ex
    else:
        return 0

    if (index_glo_ex < 0):  print("negative irrad_glo in diffuse_fraction_th\n")
    if (index_glo_ex > 1):  index_glo_ex = 1

    if (index_glo_ex <= 0.3):
        dif_frac = 1.02 - 0.254 * index_glo_ex + 0.0123 * math.sin(DTR * solar_elevation)
    if (dif_frac > 1):
        dif_frac = 1

    if (0.3 < index_glo_ex < 0.78):
        dif_frac = 1.4 - 1.749 * index_glo_ex + 0.177 * math.sin(DTR * solar_elevation)
    if (dif_frac > 0.97):
        dif_frac = 0.97
    if (dif_frac < 0.1):   dif_frac = 0.1

    if (index_glo_ex >= 0.78):
        dif_frac = 0.486 * index_glo_ex - 0.182 * math.sin(DTR * solar_elevation)
    if dif_frac < 0.1:
        dif_frac = 0.1

    return dif_frac


def calc_split(month, day, time, irrad_glo):
    jday = month_and_day_to_julian_day(month, day)

    if (irrad_glo < 0 or irrad_glo > solar_constant_e):  # / * check irradiances and exit if necessary * /
        irrad_glo = solar_constant_e

    # no object orientation yet

    solar_elevation, solar_azimuth, eccentricity_correction = solar_elev_azi_ecc(lat, lon, time_zone, jday, time)

    #

    irrad_dif = diffuse_fraction(irrad_glo, solar_elevation, eccentricity_correction) * irrad_glo

    if (solar_elevation > 5.0):

        irrad_beam_nor = (irrad_glo - irrad_dif) * 1.0 / math.sin(DTR * solar_elevation)

    else:
        irrad_beam_nor = 0
        irrad_dif = irrad_glo

    if (irrad_beam_nor > solar_constant_e):
        irrad_beam_nor = solar_constant_e
        irrad_dif = irrad_glo - irrad_beam_nor * math.sin(DTR * solar_elevation)

    print(month, day, round(time, 2), round(irrad_beam_nor, 2), round(irrad_dif, 2))

    return irrad_beam_nor, irrad_dif


lon = -103.98
lat = 1.37
time_zone = -120

print("month, day, time, irrad_beam_nor, irrad_dif\n")
calc_split(4, 22, 8.333333333, 107)
calc_split(4, 22, 8.416666667, 121)
calc_split(4, 22, 8.5, 137)
calc_split(4, 22, 8.583333333, 151)
calc_split(4, 22, 8.666666667, 159)
calc_split(4, 22, 8.75, 169)
calc_split(4, 22, 8.833333333, 178)
calc_split(4, 22, 8.916666667, 184)

# http://onebuilding.org/archive/bldg-sim-onebuilding.org/2015-May/046325.html

# Hi Phil,
#
# The gen_reindl program that comes with Daysim <http://daysim.ning.com/>
# does this pretty well, although it isn't documented on the Daysim
# website. Below is some info I sent to a student using global horizontal
# irradiation from our weather station for daylight simulation purposes.
#
# First you need to create a tab separated text file of the format *m d
# h(decimal)    gh_irrad* like the below.
#
#     4    22    8.333333333    107
#     4    22    8.416666667    121
#     4    22    8.5    137
#     4    22    8.583333333    151
#     4    22    8.666666667    159
#     4    22    8.75    169
#     4    22    8.833333333    178
#     4    22    8.916666667    184
#
# Then the gen_reindl program can be run. -l is longitude (west positive),
# -a is latitude (north positive) and -m is the time zone in a multiple of
# 15 degrees from the meridian. The command below is for Singapore, and
# you note that it is in the wrong time zone. UTC+8 * 15 = -120, despite a
# -103.98 longitude.
#  > gen_reindl -m -120 -l -103.98 -a 1.37 -i input.txt -o output.wea
#
# After running the command, the output in the output.wea file looks like
# this,
#
#     4 22 8.333 12 103
#     4 22 8.417 14 116
#     4 22 8.500 17 131
#     4 22 8.583 19 144
#     4 22 8.667 19 151
#     4 22 8.750 19 161
#     4 22 8.833 20 169
#     4 22 8.917 19 175
#
# Where the 4th column is direct normal irradiation the the 5th column is
# diffuse horizontal.
#
# Best,
# Alstan

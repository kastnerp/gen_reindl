import unittest
import numpy as np

from gen_reindl import GenReindl


def round_number(f):
    return round(f, 0)


class TestGenReindl(unittest.TestCase):

    def test_calculate_correct_result(self):
        # results taken from here: http://onebuilding.org/archive/bldg-sim-onebuilding.org/2015-May/046325.html

        # Assume

        lon = -103.98
        lat = 1.37
        time_zone = -120

        # Action



        gr = GenReindl.CreateLocation(lat, lon, time_zone)

        # Assert

        self.assertTrue(round_number(gr.calc_split(4, 22, 8.333333333, 107)[0]) == 12)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.333333333, 107)[1]) == 103)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.416666667, 121)[0]) == 14)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.416666667, 121)[1]) == 116)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.5, 137)[0]) == 17)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.5, 137)[1]) == 131)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.583333333, 151)[0]) == 19)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.583333333, 151)[1]) == 144)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.666666667, 159)[0]) == 19)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.666666667, 159)[1]) == 151)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.75, 169)[0]) == 19)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.75, 169)[1]) == 161)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.833333333, 178)[0]) == 20)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.833333333, 178)[1]) == 169)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.916666667, 184)[0]) == 19)
        self.assertTrue(round_number(gr.calc_split(4, 22, 8.916666667, 184)[1]) == 175)

    def test_calculate_correct_result_vectorized(self):
        # results taken from here: http://onebuilding.org/archive/bldg-sim-onebuilding.org/2015-May/046325.html

        # Assume

        lon = -103.98
        lat = 1.37
        time_zone = -120

        month = np.array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])

        day = np.array([22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22])

        hour = np.array(
            [8.333333333, 8.333333333, 8.416666667, 8.416666667, 8.5, 8.5, 8.583333333, 8.583333333, 8.666666667,
             8.666666667, 8.75, 8.75, 8.833333333, 8.833333333, 8.916666667, 8.916666667])

        GHR = np.array([107, 107, 121, 121, 137, 137, 151, 151, 159, 159, 169, 169, 178, 178, 184, 184])
        # Action

        gr = GenReindl.CreateLocation(lat, lon, time_zone)

        # Assert

        DNI, DHR = gr.calc_split_vectorized(gr, month, day, hour, GHR)

        self.assertTrue(round_number(DNI[0]) == 12)
        self.assertTrue(round_number(DHR[0]) == 103)
        self.assertTrue(round_number(DNI[-1]) == 19)
        self.assertTrue(round_number(DHR[-1]) == 175)


if __name__ == '__main__':
    unittest.main()

# Original cli docstring

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

# Further information

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

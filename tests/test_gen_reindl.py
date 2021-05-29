import unittest

import numpy as np

from gen_reindl import GenReindl


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

        self.assertTrue(round(gr.calc_split(4, 22, 8.33, 107)[0]) == 12)
        self.assertTrue(round(gr.calc_split(4, 22, 8.33, 107)[1]) == 103)
        self.assertTrue(round(gr.calc_split(4, 22, 8.41, 121)[0]) == 14)
        self.assertTrue(round(gr.calc_split(4, 22, 8.41, 121)[1]) == 116)
        self.assertTrue(round(gr.calc_split(4, 22, 8.50, 137)[0]) == 17)
        self.assertTrue(round(gr.calc_split(4, 22, 8.50, 137)[1]) == 131)
        self.assertTrue(round(gr.calc_split(4, 22, 8.58, 151)[0]) == 19)
        self.assertTrue(round(gr.calc_split(4, 22, 8.58, 151)[1]) == 144)
        self.assertTrue(round(gr.calc_split(4, 22, 8.66, 159)[0]) == 19)
        self.assertTrue(round(gr.calc_split(4, 22, 8.66, 159)[1]) == 151)
        self.assertTrue(round(gr.calc_split(4, 22, 8.75, 169)[0]) == 19)
        self.assertTrue(round(gr.calc_split(4, 22, 8.75, 169)[1]) == 161)
        self.assertTrue(round(gr.calc_split(4, 22, 8.83, 178)[0]) == 20)
        self.assertTrue(round(gr.calc_split(4, 22, 8.83, 178)[1]) == 169)
        self.assertTrue(round(gr.calc_split(4, 22, 8.91, 184)[0]) == 19)
        self.assertTrue(round(gr.calc_split(4, 22, 8.91, 184)[1]) == 175)

    def test_calculate_correct_result_vectorized(self):
        # results taken from here: http://onebuilding.org/archive/bldg-sim-onebuilding.org/2015-May/046325.html

        # Assume

        lon = -103.98
        lat = 1.37
        time_zone = -120

        month = np.array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])

        day = np.array([22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22])

        hour = np.array(
            [8.33,
             8.33,
             8.41,
             8.41,
             8.50,
             8.50,
             8.58,
             8.58,
             8.66,
             8.66,
             8.75,
             8.75,
             8.83,
             8.83,
             8.91,
             8.91])

        GHR = np.array([107, 107, 121, 121, 137, 137, 151, 151, 159, 159, 169, 169, 178, 178, 184, 184])
        # Action

        gr = GenReindl.CreateLocation(lat, lon, time_zone)

        # Assert

        DNI, DHR = gr.calc_split_vectorized(gr, month, day, hour, GHR)

        self.assertTrue(round(DNI[0]) == 12)
        self.assertTrue(round(DHR[0]) == 103)
        self.assertTrue(round(DNI[-1]) == 19)
        self.assertTrue(round(DHR[-1]) == 175)


if __name__ == '__main__':
    unittest.main()
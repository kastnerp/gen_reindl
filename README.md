![example workflow](https://github.com/kastnerp/gen_reindl/actions/workflows/tests.yml/badge.svg)

# gen_reindl
 Python port of `gen_reindl.exe`, a program that transforms global irradiances into horizontal diffuse and direct normal irradiances.


# Usage

## Non-vectorized

```
from gen_reindl import GenReindl

lon = -103.98
lat = 1.37
time_zone = -120

gr = GenReindl.CreateLocation(lat, lon, time_zone)
DNI, DHR = gr.calc_split(4, 22, 8.33, 107)
DNI, DHR 
```

## Vectorized

```
from gen_reindl import GenReindl

lon = -103.98
lat = 1.37
time_zone = -120

month = np.array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])

day = np.array([22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22])

hour = np.array([8.33,8.33,8.41,8.41,8.50,8.50,8.58,8.58,8.66,8.66,8.75,8.75,8.83,8.83,8.91,8.91])

GHR = np.array([107, 107, 121, 121, 137, 137, 151, 151, 159, 159, 169, 169, 178, 178, 184, 184])


gr = GenReindl.CreateLocation(lat, lon, time_zone)

DNI, DHR = gr.calc_split_vectorized(gr, month, day, hour, GHR)
DNI, DHR
```

# Comments from the original cli flags when calling `gen_reindl.exe`

## gen_reindl 

Program that transforms global irradiances into orizontal diffuse and direct normal irradiances  
_Note that the `-o` option has to be specified!_  
_Note that the `-i` option has to be specified!_  

Supported options are:  
``-i ``    input file [format: ``month`` ``day`` ``hour`` ``global_irradiation``  
``-o ``    output file [format: ``month`` ``day`` ``hour`` ``dir_norm_irrad`` ``dif_hor_irrad``  
``-m ``    time zone  
``-l ``    longitude [DEG, West is positive]  
``-a ``    latitude [DEG, North is positive]  


# More info about testing

http://onebuilding.org/archive/bldg-sim-onebuilding.org/2015-May/046325.html


````
Hi Phil,

The gen_reindl program that comes with Daysim <http://daysim.ning.com/>
does this pretty well, although it isn't documented on the Daysim
website. Below is some info I sent to a student using global horizontal
irradiation from our weather station for daylight simulation purposes.

First you need to create a tab separated text file of the format *m d
h(decimal)    gh_irrad* like the below.

    4    22    8.333333333    107
    4    22    8.416666667    121
    4    22    8.5    137
    4    22    8.583333333    151
    4    22    8.666666667    159
    4    22    8.75    169
    4    22    8.833333333    178
    4    22    8.916666667    184

Then the gen_reindl program can be run. -l is longitude (west positive),
-a is latitude (north positive) and -m is the time zone in a multiple of
15 degrees from the meridian. The command below is for Singapore, and
you note that it is in the wrong time zone. UTC+8 * 15 = -120, despite a
-103.98 longitude.
 > gen_reindl -m -120 -l -103.98 -a 1.37 -i input.txt -o output.wea

After running the command, the output in the output.wea file looks like
this,

    4 22 8.333 12 103
    4 22 8.417 14 116
    4 22 8.500 17 131
    4 22 8.583 19 144
    4 22 8.667 19 151
    4 22 8.750 19 161
    4 22 8.833 20 169
    4 22 8.917 19 175

Where the 4th column is direct normal irradiation the the 5th column is
diffuse horizontal.

Best,
Alstan

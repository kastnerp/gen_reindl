# gen_reindl
 Python port of 'gen_reindl.exe', a program that transforms global irradiances into horizontal diffuse and direct normal irradiances.


# Usage

## Non-vectorized

```
lon = -103.98
lat = 1.37
time_zone = -120

gr = GenReindl(lat, lon, time_zone)

print("irrad_beam_nor, irrad_dif\n")

```

## Vectorized

```
lon = -103.98
lat = 1.37
time_zone = -120

month = np.array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])

day = np.array([22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22])

hour = np.array([8.333333333, 8.333333333, 8.416666667, 8.416666667, 8.5, 8.5, 8.583333333, 8.583333333, 8.666666667,
     8.666666667, 8.75, 8.75, 8.833333333, 8.833333333, 8.916666667, 8.916666667])

GHR = np.array([107, 107, 121, 121, 137, 137, 151, 151, 159, 159, 169, 169, 178, 178, 184, 184])


gr = GenReindl(lat, lon, time_zone)

DNI, DHR = gr.calc_split_vectorized(gr, month, day, hour, GHR)
DNI, DHR
```

# From the original cli when calling gen_reindl.exe

gen_reindl:  
Program that transforms global irradiances into orizontal diffuse and direct normal irradiances  
Note that the -o option has to be specified!  
Note that the -i option has to be specified!  

Supported options are:  
-i     input file [format: month day hour global_irradiation  
-o     output file [format: month day hour dir_norm_irrad dif_hor_irrad  
-m     time zone  
-l     longitude [DEG, West is positive]  
-a     latitude [DEG, North is positive]  


# More info about testing

http://onebuilding.org/archive/bldg-sim-onebuilding.org/2015-May/046325.html



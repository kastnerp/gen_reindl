# gen_reindl
 Python port of 'gen_reindl.exe', a program that transforms global irradiances into orizontal diffuse and direct normal irradiances.


# Usage

```
lon = -103.98
lat = 1.37
time_zone = -120

gr = GenReindl(lat, lon, time_zone)

print("irrad_beam_nor, irrad_dif\n")
print(gr.calc_split(4, 22, 8.333333333, 107))
print(gr.calc_split(4, 22, 8.416666667, 121))
print(gr.calc_split(4, 22, 8.5, 137)
print(gr.calc_split(4, 22, 8.583333333, 151))
print(gr.calc_split(4, 22, 8.666666667, 159))
print(gr.calc_split(4, 22, 8.75, 169))
print(gr.calc_split(4, 22, 8.833333333, 178))
print(gr.calc_split(4, 22, 8.916666667, 184))
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



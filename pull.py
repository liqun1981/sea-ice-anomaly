import os

os.system("wget 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/N_seaice_extent_daily_v3.0.csv' -P Data/")
os.system("wget 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/south/daily/data/S_seaice_extent_daily_v3.0.csv' -P Data/")

for i in range(1,366):
    for H,h in zip(["north", "south"], ["N","S"]):
        url = "ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/%s/daily/shapefiles/dayofyear_median/median_extent_%s_%03d_1981-2010_polyline_v3.0.zip"%(H,h,i)
        print url
        os.system("wget '%s' -P Data/"%url)
        pass
    pass

os.system("wget 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv' -P Data/")
os.system("wget 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_  extent_sqkm.csv' -P Data/")

for y in range(2006,2020):
    for i in range(1,366):
        url = "ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/shapefiles/4km/%d/masie_ice_r00_v01_%d%03d_4km.zip"%(y,y,i)
        print url
        os.system("wget '%s' -P Data/"%url)
        pass
    pass




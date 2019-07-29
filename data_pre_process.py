import os
import pandas as pd
import datetime as dt
import glob
import zipfile
import StringIO
import shapefile


from_dir = "Data/"
to_dir = "Data_Proc/"

def parse_daily_extent_data(fname):
    f = pd.read_csv(from_dir + fname)
    f = f.drop(f.index[0])
    u = pd.DataFrame()
    u["dn"] = [dt.datetime(int(y),int(m),int(d)) for y,m,d in zip(f["Year"].tolist(), f[" Month"].tolist(), f[" Day"].tolist())]
    u["Extent"] = f["     Extent"].str.strip()
    u = u.drop(u.index[0])
    u.to_csv(to_dir + fname,header=True,index=False)
    return

fname = "N_seaice_extent_daily_v3.0.csv"
parse_daily_extent_data(fname)
fname = "S_seaice_extent_daily_v3.0.csv"
parse_daily_extent_data(fname)

def parse_daily_masie_data(fname):
    head = ["yyyyddd", " (0) Northern_Hemisphere", " (1) Beaufort_Sea",
            " (2) Chukchi_Sea", " (3) East_Siberian_Sea", " (4) Laptev_Sea",
            " (5) Kara_Sea", " (6) Barents_Sea", " (7) Greenland_Sea",
            " (8) Baffin_Bay_Gulf_of_St._Lawrence", " (9) Canadian_Archipelago",
            " (10) Hudson_Bay", " (11) Central_Arctic", " (12) Bering_Sea",
            " (13) Baltic_Sea", " (14) Sea_of_Okhotsk", " (15) Yellow_Sea",
            " (16) Cook_Inlet"]
    f = pd.read_csv(from_dir + fname, skiprows=[0])
    u = pd.DataFrame()
    f.yyyyddd = [str(y) for y in f.yyyyddd.tolist()]
    u["dn"] = [dt.datetime(int(doy[:4]),1,1)+dt.timedelta(days=int(doy[4:])-1) for doy in f.yyyyddd.tolist()]
    for h in head[1:]:
        u[h[5:]] = f[h]
        pass
    u.to_csv(to_dir + fname, header= True, index=False)
    return

fname = "masie_4km_allyears_extent_sqkm.csv"
parse_daily_masie_data(fname)

files = glob.glob("Data/median_extent_*_polyline_v3.0.zip")
for f in files:
    zipshape = zipfile.ZipFile(open(f, "rb"))
    _l = sorted(zipshape.namelist())
    sf = shapefile.Reader(shp=StringIO.StringIO(zipshape.read(_l[3])),
            shx=StringIO.StringIO(zipshape.read(_l[4])),
            dbf=StringIO.StringIO(zipshape.read(_l[1])))
    pass

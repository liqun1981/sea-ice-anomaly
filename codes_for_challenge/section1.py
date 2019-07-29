import pandas as pd
import numpy as np
from scipy import stats
import datetime as dt


# ==============================================
#  Read data chunk by chunk
# ==============================================
print "Code for section - 1"
chunksize = 100000
u = pd.DataFrame()
for df in pd.read_csv("CoBM_Parking_Citation_Data.csv",parse_dates=["ViolDate","NoticeDate","ImportDate"], chunksize=chunksize):
    u = pd.concat([u,df])
#    break
    pass
u.PoliceDistrict = u.PoliceDistrict.str.lower()
u.PoliceDistrict = u.PoliceDistrict.map({
                                            "notheastern":"northeastern", 
                                            "western":"western",
                                            "southwestern":"southwestern",
                                            "southern":"southern",
                                            "central":"central",
                                            "eastern":"eastern",
                                            "northeastern":"northeastern",
                                            "northern":"northern",
                                            "northwestern":"northwestern",
                                            "southeastern":"southeastern"
                                        })
print u.Make.unique().tolist()
u.Make = u.Make.str.lower().str[:3]
u = u[u.NoticeDate < dt.datetime(2019,1,1)]

# ===============================================
#  Estimating mean fine cost
# ===============================================
uq = u.copy()
print "Mean violation fine before 1 Jan, 2019 - %.10f"%uq.ViolFine.mean(),"\n"

# ===============================================
#  Estimating 81st percentile
# ===============================================
uq = u[(u.OpenPenalty > 0)]
print "81st percentile dolar amount of open penalty fees before 1 Jan, 2019 - %.10f"%uq.OpenPenalty.quantile(.81),"\n"

# ===================================================
#  Estimating maximum fine among 9 police districts
# ===================================================
uq = u.copy()
uq = uq.groupby("PoliceDistrict").ViolFine.mean()
print "Group by mean - ", uq.map("{:,.10f}".format),"\n"

# ===================================================================
#  Estimating top ten vehicle makes and find ratios of japanese made
# ===================================================================
uq = u.copy()
print uq.Make.unique(), len(uq.Make.unique())
uq = uq.groupby("Make").Citation.count().nlargest(10).reset_index()
print uq
models = np.array(uq.Citation)
japanese_made = models[0] + models[1] + models[4] + models[9]
total = float(models.sum())
ratio = japanese_made / total
print "Ratio - %.10f"%ratio ,"\n"


# ===============================================
#  Estimating slope of linear regression
# ===============================================
uq = u.copy()
X = np.arange(2004,2015).astype(int)
Y = []
for x in X:
    sdate, edate = dt.datetime(x,1,1),dt.datetime(x+1,1,1)
    Y.append(len(uq[(uq.ViolDate > sdate) & (uq.ViolDate < edate)]))
    pass
Y = np.array(Y)
slope, _, _, _, _ = stats.linregress(X,Y)
print "Slope of line - %.10f"%slope,"\n"


# ========================================================
#  Estimate heighest ratio of thefts to citation on 2015
# ========================================================
uq = u[(u.ViolDate >= dt.datetime(2015,1,1)) & (u.ViolDate < dt.datetime(2016,1,1))]
uq = uq.groupby("PoliceDistrict").Citation.count().reset_index()
uq = uq.rename(columns={"PoliceDistrict":"District"}).set_index("District")
du = pd.read_csv("CoBM_Police_Dept._Data.csv",parse_dates=["CrimeDate"])
du = du[(du.CrimeDate >= dt.datetime(2015,1,1)) & (du.CrimeDate < dt.datetime(2016,1,1)) & (du.District != "UNKNOWN") & (du.Description == "AUTO THEFT")]
du.District = du.District.str.lower()
du.District = du.District.map({
                                "notheast":"northeastern",
                                "western":"western",
                                "southwest":"southwestern",
                                "southern":"southern",
                                "central":"central",
                                "eastern":"eastern",
                                "northeast":"northeastern",
                                "northern":"northern",
                                "northwest":"northwestern",
                                "southeast":"southeastern"
                                })
du = du.groupby("District").Description.count().reset_index().set_index("District")
du = du.join(uq)
du["ratio"] = du["Description"] / du["Citation"]
print "Ratio - ", du.ratio.map("{:,.10f}".format),"\n"

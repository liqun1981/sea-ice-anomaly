import matplotlib 
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import seaborn as sns
from scipy import stats

sns.set_context("paper")

head = ["Beaufort_Sea", "Chukchi_Sea",
        "East_Siberian_Sea", "Laptev_Sea", "Kara_Sea", "Barents_Sea",
        "Greenland_Sea", "Baffin_Bay_Gulf_of_St._Lawrence",
        "Canadian_Archipelago", "Hudson_Bay", "Central_Arctic",
        "Bering_Sea", "Baltic_Sea", "Sea_of_Okhotsk", "Yellow_Sea",
        "Cook_Inlet"]
name = ["Beaufort Sea", "Chukchi Sea",
        "East Siberian Sea", "Laptev Sea", "Kara Sea", "Barents Sea",
        "Greenland Sea", "Baffin Bay Gulf of St. Lawrence",
        "Canadian Archipelago", "Hudson Bay", "Central Arctic",
        "Bering Sea", "Baltic Sea", "Sea of Okhotsk", "Yellow Sea",
        "Cook Inlet"]



def plot_distributions(doys):
    fig,axes  = plt.subplots(figsize=(8,8),nrows=2,ncols=2,dpi=120, sharex="all", sharey="all")
    fig.subplots_adjust(wspace = 0.1, hspace=0.1)

    I = 0
    C = ["b","r","k","g"]
    for k in doys.keys():
        doy = doys[k]
        u = np.mod(I,4)
        c = C[u]
        ax = axes[I/8,np.mod(I,2)]
        ax.plot(doy.doy,doy[k]["mean"],linewidth=.8,color=c)
        ax.fill_between(doy.doy,doy[k]["mean"]-2*doy[k]["std"],doy[k]["mean"]+2*doy[k]["std"],color=c,alpha=0.4)
        ax.set_xlim(0,365)
        I += 1
        pass
    
    ax = axes[1,0]
    ax.set_xlabel("DoY")
    ax.set_ylabel(r"$(10^6 km^2)$")

    fig.savefig("out/16_func.png",bbox_inches="tight")
    return

def distribution(fn, key, val, stats="mean", error="std"):
    fn[val] = fn[val]/1.e6
    o = fn.groupby(key).agg({val:[stats,error]}).reset_index()
    return o

def get_data(fname):
    fn = pd.read_csv(fname, parse_dates=["dn"])
    fn["yr"] = [x.to_pydatetime().year - 1978 for x in fn.dn.tolist()]
    fn["doy"] = [(x.to_pydatetime() - dt.datetime(x.to_pydatetime().year,1,1)).days + 1 for x in fn.dn.tolist()]
    fn["month"] = [x.to_pydatetime().month for x in fn.dn.tolist()]
    fn["day"] = [x.to_pydatetime().day for x in fn.dn.tolist()]
    return fn

def process_dist(fname):
    fn = get_data(fname)
    doys = {}
    for h in head:
        doys[h] = distribution(fn, "doy", h)
        pass
    return doys

doys = process_dist("Data_Proc/masie_4km_allyears_extent_sqkm.csv")
plot_distributions(doys)

ext = False
def extract_anomaly_doy(fname):
    fn = get_data(fname)
    doys = process_dist(fname)
    for k in doys.keys():
        o = doys[k]
        ano = []
        for i,x in fn.iterrows():
            a = x[k]/1.e6 - o[o.doy==x.doy][k]["mean"].tolist()[0]
            ano.append(a)
            pass
        fn[k+"_anomaly"] = ano
    fn.to_csv(fname.replace(".csv","_v2.0.csv"),header=True,index=False)
    return
if ext: extract_anomaly_doy("Data_Proc/masie_4km_allyears_extent_sqkm.csv")

def create_anomaly_intensity_trends(fname, w=30):
    fig,axes = plt.subplots(figsize=(10,5),nrows=2,ncols=2,dpi=120,sharex="row",sharey="col")
    fig.subplots_adjust(wspace = 0.1)

    C = ["r","k","b","g","r","k","b","g","r","k","b","g","r","k","b","g"] 
    I = [(0,0),(0,0),(0,0),(0,0),(0,1),(0,1),(0,1),(0,1),(1,0),(1,0),(1,0),(1,0),(1,1),(1,1),(1,1),(1,1)]
    fn = pd.read_csv(fname,parse_dates=["dn"])
    fn = fn.dropna()
    T = fn.dn.tolist()
    x = np.array([m.year - 1978 for m in T])
    i = 0
    for h,n in zip(head,name):
        d = pd.DataFrame()
        d["uano"] = fn[h+"_anomaly"].rolling(w).median()
        d["dn"] = T
        d["x"] = x
        d = d.dropna()
        s, q ,_, _, _ = stats.linregress(d.x,d.uano)
        print s, q
        u = I[i]
        ax = axes[u[0],u[1]]
        ax.plot(T,s*x+q,C[i],linewidth=0.8,label=n)
        ax.set_xlim(dt.datetime(2006,1,1), dt.datetime(2019,1,1))
        ax.set_ylim(-.1,.2)
        ax.legend(loc=1)
        i += 1
        pass
    ax = axes[1,0]
    ax.axhline(y=0,color="k",linewidth=0.5,linestyle="--")
    ax.set_xlabel("Time")
    ax.set_ylabel(r"$\alpha$" + r" $(\times 10^6 km^2)$")

    ax = axes[1,1]
    ax.set_yticklabels([])
    ax.axhline(y=0,color="k",linewidth=0.5,linestyle="--")
    ax = axes[0,1]
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.axhline(y=0,color="k",linewidth=0.5,linestyle="--")
    ax = axes[0,0]
    ax.set_xticklabels([])
    ax.axhline(y=0,color="k",linewidth=0.5,linestyle="--")
    
    fig.suptitle("Anomaly (Trends) - Substracted from DoY curve")

    fig.savefig("out/16_anomaly_intensity_trends.png",bbox_inches="tight")
    return

ext = True
if ext: create_anomaly_intensity_trends("Data_Proc/masie_4km_allyears_extent_sqkm_v2.0.csv", w = 180)

import matplotlib 
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import seaborn as sns
sns.set_context("paper")

def plot_distributions(n_doy, n_month, n_day, s_doy, s_month, s_day):
    fig,axes  = plt.subplots(figsize=(10,5),nrows=1,ncols=2,dpi=120)
    fig.subplots_adjust(wspace = 0.1)

    ax = axes[0]
    ax.plot(n_doy.doy,n_doy.Extent["mean"],"b",linewidth=.8)
    ax.fill_between(n_doy.doy,n_doy.Extent["mean"]-2*n_doy.Extent["std"],n_doy.Extent["mean"]+2*n_doy.Extent["std"],color="b",alpha=0.4)
    ax.plot(s_doy.doy,s_doy.Extent["mean"],"r",linewidth=.8)
    ax.fill_between(s_doy.doy,s_doy.Extent["mean"]-2*s_doy.Extent["std"],s_doy.Extent["mean"]+2*s_doy.Extent["std"],color="r",alpha=0.4)
    ax.set_xlabel("DoY")
    ax.set_ylabel(r"Extent $(10^6 km^2)$")
    ax.set_xlim(0,365)
    ax.set_ylim(0,20)
    ax.grid()

    ax = axes[1]
    ax.plot(n_month.month,n_month.Extent["mean"],"b",linewidth=.8)
    ax.fill_between(n_month.month,n_month.Extent["mean"]-2*n_month.Extent["std"],n_month.Extent["mean"]+2*n_month.Extent["std"],color="b",alpha=0.4)
    ax.plot(s_month.month,s_month.Extent["mean"],"r",linewidth=.8)
    ax.fill_between(s_month.month,s_month.Extent["mean"]-2*s_month.Extent["std"],s_month.Extent["mean"]+2*s_month.Extent["std"],color="r",alpha=0.4)
    ax.set_xlabel("Month")
    ax.set_xlim(1,12)
    ax.set_ylim(0,20)
    ax.set_yticklabels([])
    ax.grid()

    fig.savefig("out/distribution.png",bbox_inches="tight")
    return

def distribution(fn, key, stats="mean", error="std"):
    o = fn.groupby(key).agg({"Extent":[stats,error]}).reset_index()
    return o

def get_data(fname):
    fn = pd.read_csv(fname, parse_dates=["dn"])
    fn["yr"] = [x.to_pydatetime().year - 1978 for x in fn.dn.tolist()]
    fn["doy"] = [(x.to_pydatetime() - dt.datetime(x.to_pydatetime().year,1,1)).days + 1 for x in fn.dn.tolist()]
    fn["month"] = [x.to_pydatetime().month for x in fn.dn.tolist()]
    fn["day"] = [x.to_pydatetime().day for x in fn.dn.tolist()]
    fn.drop(["dn"],axis=1, inplace=True)
    return fn

def process_dist(fname):
    fn = get_data(fname)

    o_doy_mean = distribution(fn, key="doy")
    o_month_mean = distribution(fn, key="month")
    o_day_mean = distribution(fn, key="day")

    o_doy_med = distribution(fn, key="doy", stats="median")
    o_month_med = distribution(fn, key="month", stats="median")
    o_day_med = distribution(fn, key="day", stats="median")
    return o_doy_mean,o_month_mean,o_day_mean,o_doy_med,o_month_med,o_day_med

n_doy, n_month, n_day, _, _, _ = process_dist("Data_Proc/N_seaice_extent_daily_v3.0.csv")
s_doy, s_month, s_day, _, _, _ = process_dist("Data_Proc/S_seaice_extent_daily_v3.0.csv")
plot_distributions(n_doy, n_month, n_day, s_doy, s_month, s_day)

ext = False
def extract_anomaly_doy(fname):
    fn = get_data(fname)
    o = distribution(fn, key="doy")
    ano = []
    for i,x in fn.iterrows():
        a = x.Extent - o[o.doy==x.doy].Extent["mean"].tolist()[0]
        ano.append(a)
        pass
    fn["anomaly"] = ano
    fn.to_csv(fname.replace("v3.0","v4.0"),header=True,index=False)
    return
if ext:
    extract_anomaly_doy("Data_Proc/N_seaice_extent_daily_v3.0.csv")
    extract_anomaly_doy("Data_Proc/S_seaice_extent_daily_v3.0.csv")

def extract_anomaly_by_days(fname, n_day):
    fn = get_data(fname)
    fn["anomaly"] = np.array(fn.Extent - fn.Extent.rolling(n_day).mean())
    fn.to_csv(fname.replace("v3.0","v4.0").replace("daily","(%003d)Days"%n_day),header=True,index=False)
    return

n_day_anomaly = [5,10,15,30,60,180,365]
fnames = ["Data_Proc/N_seaice_extent_daily_v3.0.csv","Data_Proc/S_seaice_extent_daily_v3.0.csv"]
for n_day in n_day_anomaly:
    for fname in fnames:
        if ext: extract_anomaly_by_days(fname, n_day)
        pass
    pass

def histograms(n_fname, s_fname, png_name, low=-2.8, high=2.8):
    fig,axes = plt.subplots(figsize=(5,5),nrows=1,ncols=1,dpi=120)
    fig.subplots_adjust(wspace = 0.1)

    fn = pd.read_csv(n_fname)
    fn = fn.dropna()
    ax = axes
    ax.grid()
    ax.hist(fn.anomaly,bins="auto",normed=True,histtype="step", color="b",linewidth=0.8, label="North")
    ax.set_xlabel(r"$\alpha_N$")
    ax.set_ylabel(r"$f(\alpha)$")
    ax.set_xlim(low,high)

    fn = pd.read_csv(s_fname)
    fn = fn.dropna()
    ax.hist(fn.anomaly,bins="auto",normed=True,histtype="step",color="r",linewidth=0.8, label="South")
    ax.set_xlim(low,high)
    ax.set_xlabel(r"$\alpha_S$")
    ax.legend(loc=1)

    fig.suptitle("Anomaly - Substracted from mean DoY curve")
    fig.savefig(png_name,bbox_inches="tight")
    return

ext = False
if ext:
    histograms("Data_Proc/N_seaice_extent_daily_v4.0.csv","Data_Proc/S_seaice_extent_daily_v4.0.csv","out/anomaly_ext_using_doy.png")
    histograms("Data_Proc/N_seaice_extent_(005)Days_v4.0.csv","Data_Proc/S_seaice_extent_(005)Days_v4.0.csv","out/anomaly_ext_using_(005)Days.png",-1.,1.)
    histograms("Data_Proc/N_seaice_extent_(010)Days_v4.0.csv","Data_Proc/S_seaice_extent_(010)Days_v4.0.csv","out/anomaly_ext_using_(010)Days.png",-1.5,1.5)
    histograms("Data_Proc/N_seaice_extent_(015)Days_v4.0.csv","Data_Proc/S_seaice_extent_(015)Days_v4.0.csv","out/anomaly_ext_using_(015)Days.png",-2.,2.)
    histograms("Data_Proc/N_seaice_extent_(030)Days_v4.0.csv","Data_Proc/S_seaice_extent_(030)Days_v4.0.csv","out/anomaly_ext_using_(030)Days.png",-2.5,2.5)
    histograms("Data_Proc/N_seaice_extent_(060)Days_v4.0.csv","Data_Proc/S_seaice_extent_(060)Days_v4.0.csv","out/anomaly_ext_using_(060)Days.png",-3.,3.)
    histograms("Data_Proc/N_seaice_extent_(180)Days_v4.0.csv","Data_Proc/S_seaice_extent_(180)Days_v4.0.csv","out/anomaly_ext_using_(180)Days.png",-3.5,3.5)
    histograms("Data_Proc/N_seaice_extent_(365)Days_v4.0.csv","Data_Proc/S_seaice_extent_(365)Days_v4.0.csv","out/anomaly_ext_using_(365)Days.png",-4.,4.)

def create_anomaly_intensity_trends(n_fname, s_fname,u=30):
    fig,axes = plt.subplots(figsize=(10,5),nrows=1,ncols=2,dpi=120)
    fig.subplots_adjust(wspace = 0.1)

    fn = pd.read_csv(n_fname)
    fn = fn.dropna()
    T = [dt.datetime(y+1978,1,1) + dt.timedelta(x) for y,x in zip(fn.yr.tolist(),fn.doy.tolist())]
    ano = fn.anomaly.rolling(u).median()
    ano_std = fn.anomaly.rolling(u).std()
    ax = axes[0]
    ax.plot(T,ano,color="b",linewidth=0.8)
    ax.fill_between(T,ano-2*ano_std,ano+2*ano_std,color="b",alpha=0.4)
    ax.set_xlabel("Time")
    ax.set_ylabel(r"$\alpha$"+r" $(\times 10^6 km^2)$")
    ax.set_xlim(dt.datetime(1980,1,1), dt.datetime(2020,1,1))
    ax.set_ylim(-3,3)
    ax.grid()

    fn = pd.read_csv(s_fname)
    fn = fn.dropna()
    T = [dt.datetime(y+1978,1,1) + dt.timedelta(x) for y,x in zip(fn.yr.tolist(),fn.doy.tolist())]
    ano = fn.anomaly.rolling(u).median()
    ano_std = fn.anomaly.rolling(u).std()
    ax = axes[1]
    ax.plot(T,ano,color="r",linewidth=0.8)
    ax.fill_between(T,ano-2*ano_std,ano+2*ano_std,color="r",alpha=0.4)
    ax.set_xlabel("Time")
    ax.set_ylim(-3,3)
    ax.set_yticklabels([])
    ax.set_xlim(dt.datetime(1980,1,1), dt.datetime(2020,1,1))
    ax.grid()

    fig.suptitle("Anomaly (Trends) - Substracted from DoY curve")

    fig.savefig("out/anomaly_intensity_trends.png",bbox_inches="tight")
    return

create_anomaly_intensity_trends("Data_Proc/N_seaice_extent_daily_v4.0.csv","Data_Proc/S_seaice_extent_daily_v4.0.csv", u = 180)

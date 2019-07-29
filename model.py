import numpy as np
import pandas as pd
import datetime as dt
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

seed = 0
np.random.seed(seed)

def get_data(fname):
    f = pd.read_csv(fname)
    return f

def deep_model(n_layer=5,nodes_per_layer={0:80,1:80,2:80,3:80,4:80},input_dim=4):
    m = Sequential()
    m.add(Dense(input_dim, input_dim=input_dim, kernel_initializer="normal", activation="relu"))
    for i in np.arange(n_layer):
        m.add(Dense(nodes_per_layer[i], kernel_initializer="normal", activation="relu"))
        pass
    m.add(Dense(1, kernel_initializer="normal", activation="linear"))
    m.compile(loss="mean_squared_error", optimizer="adam")
    return m

def model(hemi="N"):
    f = get_data("Data_Proc/%s_seaice_extent_daily_v4.0.csv"%hemi)
    X = f[["yr","month","doy","day"]].as_matrix()
    y = f["Extent"].as_matrix()
    scaler = MinMaxScaler()
    scaler.fit(X)
    
    m = KerasRegressor(build_fn=deep_model, epochs=50, batch_size=100, verbose=0)
    kfold = KFold(n_splits=10, random_state=seed)
    results = cross_val_score(m, X, y, cv=kfold)
    print("Standardized: %.2f (%.2f) MSE" % (results.mean(), results.std()))

    m.fit(X,y)
    m.model.save("Data_Proc/%s_model.h5"%hemi)
    return

ext = False
if ext:
    model()
    model("S")


def predictions(hemi="N",start_time=dt.datetime(2019,1,1), timedelta = 365):
    f = get_data("Data_Proc/%s_seaice_extent_daily_v4.0.csv"%hemi)
    X = f[["yr","month","doy","day"]].as_matrix()

    dn = [start_time + dt.timedelta(x) for x in np.arange(timedelta)]
    u = pd.DataFrame()
    u["yr"] = [x.year-1978 for x in dn]
    u["month"] = [x.month for x in dn]
    u["day"] = [x.day for x in dn]
    u["doy"] = [(x - dt.datetime(x.year,1,1)).days + 1 for x in dn]
    Xp = u[["yr","month","doy","day"]].as_matrix()
    print Xp.shape
    Xn = np.concatenate((X,Xp))
    print Xn.shape,X.shape
    scaler = MinMaxScaler()
    scaler.fit(Xn)
    x = scaler.transform(Xp)

    m = KerasRegressor(build_fn=deep_model, epochs=50, batch_size=100, verbose=0)
    m.model = load_model("Data_Proc/%s_model.h5"%hemi)
    y = m.predict(x)
    print y,x
    #o = distribution(f, key="doy")
    #ano = []
    #for x,doy in zip(y,u.doy.tolist()):
    #    a = x - o[o.doy==doy].Extent["mean"].tolist()[0]
    #    ano.append(a)
    #    pass
    #print ano
    return
predictions()

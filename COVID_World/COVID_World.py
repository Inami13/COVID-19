import pandas as pd
from datetime import date, timedelta

day = date.today()
try:
    url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-%s.xlsx"%day.strftime("%Y-%m-%d")
    df = pd.read_excel(url)
except:
    day = date.today() - timedelta(days=1)
    try:
        url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-%s.xlsx"%day.strftime("%Y-%m-%d")
        df = pd.read_excel(url)
    except:
        day = date.today() - timedelta(days=2)
        try:
            url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-%s.xlsx"%day.strftime("%Y-%m-%d")
            df = pd.read_excel(url)
        except:
            raise SystemExit("\nNo reports in the last two days.\n")

df = df.rename(columns = {'dateRep':'DateRep','cases':'Cases','deaths':'Deaths','countriesAndTerritories':'Countries and territories','geoId':'GeoId'}) 

def computeMACD(values, short, long, lag):
    macd   = computeEMA(values, short) - computeEMA(values, long)
    signal = computeEMA(macd, lag)
    hist   = macd - signal
    return macd, signal, hist

def computeEMA(values, period):    
    return values.ewm(span=period,min_periods=0,adjust=False,ignore_na=False).mean()


C = df.groupby('GeoId')['Cases'].agg(["sum","first"]).rename_axis([""])
D = df.groupby('GeoId')['Deaths'].agg(["sum","first"]).rename_axis([""])

layer = QgsProject.instance().mapLayersByName('Total_Cases')[0]
features = layer.getFeatures()

layer.startEditing()

for feature in features:
    # retrieve every feature with its geometry and attributes
    ID = feature['ISO_A2']
    Pop = float(feature['POP_EST'])
    if ID in C.index:
        v = df[df['GeoId'] == ID][['Cases','Deaths']].iloc[::-1]
        HIST = [0,0]
        for i in range(len(v.keys())):            
            hist = list(computeMACD(v[v.columns[i]], 14, 21, 9)[2])
            HIST[i] = hist[-1]
        
        layer.changeAttributeValue(feature.id(), 16, int(C.loc[ID][0]))
        layer.changeAttributeValue(feature.id(), 17, int(C.loc[ID][1]))
        layer.changeAttributeValue(feature.id(), 18, int(D.loc[ID][0]))
        layer.changeAttributeValue(feature.id(), 19, int(D.loc[ID][1]))
        layer.changeAttributeValue(feature.id(), 20, float(C.loc[ID][0])/Pop*1000000)
        layer.changeAttributeValue(feature.id(), 21, float(D.loc[ID][0])/Pop*1000000)
        layer.changeAttributeValue(feature.id(), 22, float(HIST[0]))
        layer.changeAttributeValue(feature.id(), 23, float(HIST[1]))
    else:
        layer.changeAttributeValue(feature.id(), 16, 0)
        layer.changeAttributeValue(feature.id(), 17, 0)
        layer.changeAttributeValue(feature.id(), 18, 0)
        layer.changeAttributeValue(feature.id(), 19, 0)
        layer.changeAttributeValue(feature.id(), 20, 0)
        layer.changeAttributeValue(feature.id(), 21, 0)
        layer.changeAttributeValue(feature.id(), 22, 0)
        layer.changeAttributeValue(feature.id(), 23, 0)
        
layer.commitChanges()

day = day - timedelta(days=1)
print('Last updated data:\t%s' %day.strftime("%d-%m-%Y"))
    

    
    

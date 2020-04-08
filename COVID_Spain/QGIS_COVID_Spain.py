import pandas as pd

df = pd.read_csv('https://covid19.isciii.es/resources/serie_historica_acumulados.csv',delimiter=',',encoding = 'unicode_escape')

df['FECHA']= pd.to_datetime(df['FECHA'], dayfirst = True)
df = df.sort_values(['CCAA', 'FECHA'])

def computeMACD(values, short, long, lag):
    macd   = computeEMA(values, short) - computeEMA(values, long)
    signal = computeEMA(macd, lag)
    hist   = macd - signal
    return macd, signal, hist

def computeEMA(values, period):    
    return values.ewm(span=period,min_periods=0,adjust=False,ignore_na=False).mean()

layer = QgsProject.instance().mapLayersByName('Total casos')[0]
features = layer.getFeatures()

layer.startEditing()

for feature in features:
    # retrieve every feature with its geometry and attributes
    ID = str(feature['Codigo'])
    Pop = float(feature['Población'])
    
    Casos = df[df['CCAA'] == ID]['CASOS'].fillna(0)
    Fallecidos = df[df['CCAA'] == ID]['Fallecidos'].fillna(0)
    
    layer.changeAttributeValue(feature.id(), 3, int(Casos.iloc[-1]))    
    layer.changeAttributeValue(feature.id(), 4, float(Casos.iloc[-1]/Pop*100000))
    layer.changeAttributeValue(feature.id(), 5, int(Fallecidos.iloc[-1]))    
    layer.changeAttributeValue(feature.id(), 6, float(Fallecidos.iloc[-1]/Pop*100000))
    
    
    v = Casos.diff()
    v.iloc[0] = Casos.iloc[0]
    layer.changeAttributeValue(feature.id(), 7, int(v.iloc[-1]))
    hist = list(computeMACD(v, 14, 21, 9)[2])
    layer.changeAttributeValue(feature.id(), 9, float(hist[-1]))
    
    v = Fallecidos.diff()
    v.iloc[0] = Fallecidos.iloc[1]
    layer.changeAttributeValue(feature.id(), 8, int(v.iloc[-1]))
    hist = list(computeMACD(v, 14, 21, 9)[2])
    layer.changeAttributeValue(feature.id(), 10, float(hist[-1]))

layer.commitChanges()

print('\nFecha de actualización de los datos: %s'%(df.groupby('FECHA').any().index[-1]))
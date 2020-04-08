import pandas as pd

df = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7',delimiter=';')

df = df[df['sexe'] == 0].sort_values(['dep','jour'])

def computeMACD(values, short, long, lag):
    macd   = computeEMA(values, short) - computeEMA(values, long)
    signal = computeEMA(macd, lag)
    hist   = macd - signal
    return macd, signal, hist

def computeEMA(values, period):    
    return values.ewm(span=period,min_periods=0,adjust=False,ignore_na=False).mean()

layer = QgsProject.instance().mapLayersByName('Total_Décès')[0]
features = layer.getFeatures()   

layer.startEditing()

for feature in features:
    # retrieve every feature with its geometry and attributes
    ID = str(feature['code_insee'])
    Pop = float(feature['Population'])    
    dep = list(df.groupby('dep').first().index)
    if ID in dep:
        dc = df[df['dep'] == ID]['dc']
        layer.changeAttributeValue(feature.id(), 5, int(dc.iloc[-1]))
        layer.changeAttributeValue(feature.id(), 6, float(dc.iloc[-1]/Pop*100000))
        v = dc.diff()
        v.iloc[0] = dc.iloc[0]
        layer.changeAttributeValue(feature.id(), 7, int(v.iloc[-1]))
        hist = list(computeMACD(v, 14, 21, 9)[2])
        layer.changeAttributeValue(feature.id(), 8, float(hist[-1]))
    else:
        layer.changeAttributeValue(feature.id(), 5, 0)
        layer.changeAttributeValue(feature.id(), 6, 0)
        layer.changeAttributeValue(feature.id(), 7, 0)
        layer.changeAttributeValue(feature.id(), 8, 0)

layer.commitChanges()

print('\nDate de actualisation des données : %s'%(df.groupby('jour').any().index[-1]))
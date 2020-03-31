# COVID-19

Data visualization, using Python and QGIS, of the evolution of the COVID-19 at different scales and detail depending on the data provided by the official sources. Three different studies have been made for France, Spain and the world.

## QGIS

In order to display data in maps, QGIS is required along with the provided vectorial layers of administrative divisions. Most of ShapeFile layers provided in this repository need to be unzipped before usage. The Spain project uses an extra layer that is not included due to size issues, but it can be downloaded from the following [link](http://opendata.esri.es/datasets/poblaci%C3%B3n-total-por-municipios-padr%C3%B3n-2015) or discarded since it is not essential for COVID-19 understanding (it just adds extra information of municipalities by population density).

A Python script is provided with each of the QGIS projects and should be run in the built-in Python console after openning the project. The script will automatically download the latest available data and update the attribute table of the layers.

A rescaling of the colorbars could be necessary in order to correctly visualize the new data.

Some map infographies are provided as examples. See **About the acceleration** for more information about the method followed for the computation of the acceleration.

## Python script

For the world data, a Python script is also provided, independant from the QGIS project. This script downloads the last updated data from the European Centre for Disease Prevention and Control and two different built-in functions provide statistics of the COVID-19.

Worldmetrics shows the current top 10 countries in terms of:

 * Cases
 * Cases normalized by population
 * Deaths
 * Deaths normalized by population
 
Some plots show the chronological evolution of the disease for the top 10 countries. New cases and deaths are smoothed using an Exponential Moving Average ([EMA](https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average)) of 14 days, i.e. the maximum incubation time of the COVID-19.

CountryMACD shows the situation for a specific country. Country names should be given using underscore for the spaces (e.g. United_States_of_America).

## About the acceleration

In order to visualize the acceleration or deceleration of new cases and deaths, an innovative idea of using trading indicators to follow the trends has been implemented. 

The Moving Average Convergence Divergence ([MACD](https://en.wikipedia.org/wiki/MACD)), commonly used to in technical analysis of stock prices, has been chosen. This indicator compares the EMA for two different time periods (usually 12 and 26 days). A Signal Line is the performed applying an EMA of a shorter time to the MACD (usually 9 day-period). The difference between the MACD and the Signal Line gives an idea of the acceleration of the price.

For this project, in order to be more representative of the disease, periods of 14 and 21 days have been chosen as default values (still 9 days for the Signal Line). Nevertheless, results do not change significantly by using these new values compared to the classical ones. Anyway, the code has been left open to experiment with different values as you wish.

Since this method is based on EMA, it has an inherent lag so a change in the trend will take a few days before it is clearly shown in the acceleration curve. This is in fact a desired effect for this specific case, since the curve of new cases/deaths is often pretty noisy, and a 24h change doesn't necessarily mean an overall change on the trends.

In QGIS maps, the value shown is the most recent value of the acceleration curve.

## Authors

* **[Ivan Deiros](https://github.com/Inami13)** - *Initial work*
* **[Oscar Argudo](https://github.com/oargudo)** - *Code for MACD computation and plots*

## Sources

### Data

* World: [European Centre for Disease Prevention and Control](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide) (ECDC)
* France: [Santé publique France](https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/)
* Spain: [Ministerio de Sanidad](https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm) (Gobierno de España)

### Maps

Different open source maps. See the respective QGIS layers for more information about the coresponding source and version.

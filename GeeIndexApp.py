from greppo import app
import geopandas as gpd
import pandas as pd
import numpy as np
import ee
from datetime import date 

today = date.today() 
today = today.strftime("%Y-%m-%d")

email = "potatoapp@potatoapp-358001.iam.gserviceaccount.com"
key_file = './Key/key_file.json'
credentials = ee.ServiceAccountCredentials(email=email, key_file=key_file)
ee.Initialize(credentials)

# Select the satellite dataset from the catalog
dem = ee.Image('USGS/SRTMGL1_003')
ee_dem = dem.updateMask(dem.gt(0))
vis_params = {
    'min': 0,
    'max': 4000,
    'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}

ndvi = ee.ImageCollection('MODIS/MCD43A4_006_NDVI') \
                .filterDate('2022-01-01', today) \
                .first()
              
ndviVis = {
  'min': 0.0,
  'max': 1.0,
  'palette': [
    'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
    '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
    '012E01', '011D01', '011301'
  ],
}

evi = ee.ImageCollection('MODIS/MCD43A4_006_EVI') \
                .filterDate('2022-01-01', today) \
                .first()
              
eviVis = {
  'min': 0.0,
  'max': 1.0,
  'palette': [
    'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
    '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
    '012E01', '011D01', '011301'
  ],
}

ndsi = ee.ImageCollection('MODIS/MCD43A4_006_NDSI') \
                .filterDate('2022-01-01', today) \
                .first()

ndsiVis = {
  'palette': ['000088', '0000FF', '8888FF', 'FFFFFF'],
}

bai = ee.ImageCollection('MODIS/MCD43A4_006_BAI') \
                .filterDate('2022-01-01', today) \
                .first()

baiVis = {
  min: 0.0,
  max: 100.0,
}

ndwi = ee.ImageCollection('MODIS/MCD43A4_006_NDWI') \
                .filterDate('2022-01-01', today) \
                .first()

ndwiVis = {
  'min': 0.0,
  'max': 1.0,
  'palette': ['0000ff', '00ffff', 'ffff00', 'ff0000', 'ffffff'],
}

app.ee_layer(ee_object=ndsi, vis_params=ndsiVis , name='NDSI', 
             description='World Digital NDSI from GEE', visible = True)

app.ee_layer(ee_object=bai, vis_params=baiVis , name='BAI', 
             description='World Digital BAI from GEE', visible = True)

app.ee_layer(ee_object=ndwi, vis_params=ndwiVis , name='NDWI', 
             description='World Digital NDWI from GEE', visible = True)

app.ee_layer(ee_object=ee_dem, vis_params=vis_params, name='DEM', 
             description='World Digital Elevation Map from GEE', visible = True)

app.ee_layer(ee_object=evi, vis_params=eviVis , name='EVI', 
             description='World Digital EVI from GEE', visible = True)

app.ee_layer(ee_object=ndvi, vis_params=ndviVis, name='NDVI', 
             description='World Digital NDVI from GEE', visible = True)


app.display(name='text1', value='# Enter point value for finding corresponding spectral indexes values')

lon = app.number(name='Longitude of the point', value= -74)
lat = app.number(name='Latitude of the point', value= 2)
point_name = app.text(name='Enter the name of point', value='Sample point')

# Point object in EE
ee_point = ee.Geometry.Point([lon, lat])
app.ee_layer(ee_object=ee_point, vis_params={"color": "red",
  "width": 10}, 
             name=point_name, description= f"The Point representing {point_name}.")

## BASEMAPS

app.base_layer(
    name="CartoDB Light",
    visible=False,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

app.base_layer(
    name="Open Street Map",
    visible=False,
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

app.base_layer(
    name="Google Hybrid",
    visible=True,
    url='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    subdomains=None,
)


# Display the elevation
elev = ee_dem.sample(ee_point).first()
elev = elev.get('elevation').getInfo()

ndviv = ndvi.sample(ee_point).first()
ndviv = ndviv.get('NDVI').getInfo()

eviv = evi.sample(ee_point).first()
eviv = eviv.get('EVI').getInfo()

ndsiv = ndsi.sample(ee_point).first()
ndsiv = ndsiv.get('EVI').getInfo()

baiv = bai.sample(ee_point).first()
baiv = baiv.get('EVI').getInfo()

ndwiv = ndwi.sample(ee_point).first()
ndwiv = ndwiv.get('NDWI').getInfo()

elev_text = f"""
# Point: {point_name}
## Coordinate: (Lon: {lon}, Lat: {lat})
## Elevation: {elev} m
## NDVI: {ndviv}
## EVI: {eviv}
## NDSI: {ndsiv}
## BAI: {baiv}
## NDWI: {ndwiv}
"""
app.display(name='elev-text', value=elev_text)

app.map(center=[lat, lon], zoom=5)
import pandas as pd
import os

os.chdir('C:/Users/TAN/Documents/IM/RealEstateProject/')
#xl_file = pd.ExcelFile()
dfs = pd.read_excel('tmp_2020-03-21.xlsx', sheet_name='Sheet1',index_col=0)

dfs

dfs['totalarea'] = dfs['totalarea'].astype('str')
#dfs['totalarea'] = dfs['totalarea'].map(lambda x: x.rstrip(' m²'))
#df_out=dfs
#dfs[~dfs.totalarea.str.contains(" m²")]

#FOr comparing new prices

dfs2 = pd.read_excel('tmp_2020-03-25.xlsx', sheet_name='Sheet1',index_col=0)

#dfs.where(dfs.geoloc==dfs2.geoloc).notna()
dfs.geoloc.dtype  
dfs['geoloc'] = dfs['geoloc'].astype('str')
dfs2['geoloc'] = dfs2['geoloc'].astype('str')
#dfs.where(dfs.geoloc==dfs2.geoloc).notna()
c=0

#dfs[dfs.numoffloor.str.contains(" m²")]

#print(dfs.numoffloor.isin(dfs.totalarea))
#dfs['numoffloor'].loc[dfs.numoffloor.str.contains(" m²")] = 10

#if numoffloor contains " m²", it will swap values of totalarea and numoffloor. 
mask = (dfs.numoffloor.str.contains(" m²",na=False))
n=dfs['numoffloor'][mask]
dfs['numoffloor'][mask] = dfs['totalarea'][mask]
dfs['totalarea'][mask] = n
dfs.iloc[82:85,:]

import numpy as np

#If totalarea contains ":", it will replace them with NaN
mask = (dfs.totalarea.str.contains(":",na=False))
dfs['totalarea'][mask] = np.NaN

#if totalarea contains "Kinnistu", it will replace them with NaN
mask = (dfs.totalarea.str.contains("Kinnistu",na=False))
dfs['totalarea'][mask] = np.NaN

#if totalarea contains "/", it will copy the specific totalarea value and replace numoffloor with that value and replace totalarea with NaN
mask = (dfs.totalarea.str.contains("/",na=False))
#n=dfs['totalarea'][mask]
dfs['numoffloor'][mask] = dfs['totalarea'][mask]
dfs['totalarea'][mask] = np.NaN

#dfs


#if totalarea contains "Reno, And", it will replace them with NaN
mask = (dfs.totalarea.str.contains("Reno",na=False))
dfs['totalarea'][mask] = np.NaN
mask = (dfs.totalarea.str.contains("And",na=False))
dfs['totalarea'][mask] = np.NaN

#If there totalarea does not have value that contains " m²", it will replace them with NaN
mask = (~dfs.totalarea.str.contains(" m²",na=False))
dfs['totalarea'][mask] = np.NaN

#dfs.loc[222:227,:]


#if landarea does not contain value without " m²", it will replace them with NaN
mask = (~dfs.landarea.str.contains(" m²",na=False))
dfs['landarea'][mask] = np.NaN

#if rooms contain " m²", it will replace them with NaN
mask = (dfs.rooms.str.contains(" m²",na=False))
dfs['rooms'][mask] = np.NaN
mask = (dfs.rooms.str.contains("-",na=False))
dfs['rooms'][mask] = np.NaN
dfs.loc[dfs['rooms'].str.len() >= 3, 'rooms'] = np.nan

#if numoffloor contains "Tea,V", it will replace them with NaN
mask = (dfs.numoffloor.str.contains("Tea",na=False))
dfs['numoffloor'][mask] = np.NaN
mask = (dfs.numoffloor.str.contains("V",na=False))
dfs['numoffloor'][mask] = np.NaN


#if numoffloor contain "Ren", it will copy the value to condition and replace numoffloor with NaN
mask = (dfs.numoffloor.str.contains("Ren",na=False))
#n=dfs['totalarea'][mask]
dfs['condition'][mask] = dfs['numoffloor'][mask]
dfs['numoffloor'][mask] = np.NaN

#if numoffloor contain "And", it will copy the value to condition and replace numoffloor with NaN
mask = (dfs.numoffloor.str.contains("And",na=False))
#n=dfs['totalarea'][mask]
dfs['condition'][mask] = dfs['numoffloor'][mask]
dfs['numoffloor'][mask] = np.NaN

#if numoffloor contain "Heas", it will copy the value to condition and replace numoffloor with NaN
mask = (dfs.numoffloor.str.contains("Heas",na=False))
#n=dfs['totalarea'][mask]
dfs['condition'][mask] = dfs['numoffloor'][mask]
dfs['numoffloor'][mask] = np.NaN

#if numoffloor contain "Kinnis", it will replace numoffloor with NaN
mask = (dfs.numoffloor.str.contains("Kinnis",na=False))
#n=dfs['totalarea'][mask]
#dfs['condition'][mask] = dfs['numoffloor'][mask]
dfs['numoffloor'][mask] = np.NaN


#if numoffloor contain ":", it will replace numoffloor with NaN
mask = (dfs.numoffloor.str.contains(":",na=False))
#n=dfs['totalarea'][mask]
#dfs['condition'][mask] = dfs['numoffloor'][mask]
dfs['numoffloor'][mask] = np.NaN


#if numoffloor contain string with length greater than 6, it will replace numoffloor with NaN
dfs.loc[dfs['numoffloor'].str.len() >= 6, 'numoffloor'] = np.nan

#if numoffloor contain "-", it will replace numoffloor with NaN
mask = (dfs.numoffloor.str.contains("-",na=False))
dfs['numoffloor'][mask] = np.NaN


#if energymark contain "-", it will replace energymark with NaN
mask = (dfs.energymark.str.contains("-",na=False))
dfs['energymark'][mask] = np.NaN

#if energymark contain "Puudub", it will replace energymark with NaN
mask = (dfs.energymark.str.contains("Puudub",na=False))
dfs['energymark'][mask] = np.NaN

#stripping m² from total area and dtype=float
dfs['totalarea'] = dfs['totalarea'].astype('str')
dfs['totalarea'] = dfs['totalarea'].map(lambda x: x.rstrip(' m²'))
dfs['totalarea'] = dfs['totalarea'].astype('float')

#stripping m² from total area and dtype=float
dfs['landarea'] = dfs['landarea'].astype('str')
dfs['landarea'] = dfs['landarea'].map(lambda x: x.rstrip(' m²'))
dfs['landarea'] = dfs['landarea'].astype('float')

#if price contain "U..", it will replace energymark with NaN
dfs['price'] = dfs['price'].astype('str')
mask = (dfs.price.str.contains("U"))
dfs['price'][mask] = np.NaN

#if price contain " ", it will strip them
dfs['price'] = dfs['price'].str.replace(r'\D', '')
dfs['price'] =dfs.price.replace('',np.NaN)
dfs['price'] = dfs['price'].astype('float')

##if pricesqm contain " €/m2", it will strip them
dfs['pricesqm'] = dfs['pricesqm'].astype('str')
dfs['pricesqm'] = dfs['pricesqm'].map(lambda x: x.rstrip(' €/m2'))
dfs['pricesqm'] = dfs['pricesqm'].str.replace(r'\D', '')

##if pricesqm contain "", it will replace them with NaN
dfs['pricesqm'] =dfs.pricesqm.replace('',np.NaN)
dfs['pricesqm'] = dfs['pricesqm'].astype('float')

##if builtyear contain "", it will replace them with NaN
dfs['builtyear'] =dfs.builtyear.replace('',np.NaN)
dfs['builtyear'] = dfs['builtyear'].astype('float')

##if rooms contain "", it will replace them with NaN
dfs['rooms'] =dfs.rooms.replace('',np.NaN)
dfs['rooms'] = dfs['rooms'].astype('float')

dfs['geoloc'] = dfs['geoloc'].astype('str')


#save preprocessed data
from pandas import ExcelWriter
writer = ExcelWriter('preprocessed_data.xlsx')
dfs.to_excel(writer,'Sheet1')
writer.save()
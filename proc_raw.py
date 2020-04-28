import numpy as np
import pandas as pd


def split_and_get(df):
    df = df.loc[:, ~df.columns.str.match('^Unnamed')]
    df['listing_type'] = df['name'].str.split(',').str[0].str.split('-').str[0]  # Get the ad type
    df['county'] = df['name'].str.split(',').str[-1]
    df['listing_type'] = df['listing_type'].str.strip()
    df["obj_type"] = ""
    df.loc[df['listing_type'].str.contains("korter") == True, 'obj_type'] = 'apartment'
    df.loc[df['listing_type'].str.contains("äripind") == True, 'obj_type'] = 'commercial_space'
    df.loc[df['listing_type'].str.contains("maja") == True, 'obj_type'] = 'house'
    df.loc[df['listing_type'].str.contains("majaosa") == True, 'obj_type'] = 'house_part'
    df.loc[df['listing_type'].str.contains("ridaelamuboks") == True, 'obj_type'] = 'terraced house'
    df.loc[df['listing_type'].str.contains("maatükk") == True, 'obj_type'] = 'land'
    df.loc[df['listing_type'].str.contains("talu") == True, 'obj_type'] = 'farm'
    df.loc[df['listing_type'].str.contains("suvila") == True, 'obj_type'] = 'cottage'
    df.loc[df['listing_type'].str.contains("garaaž") == True, 'obj_type'] = 'garage'
    df.loc[df['listing_type'].str.contains("muu") == True, 'obj_type'] = 'other'
    df.loc[df['listing_type'].str.contains("Müüa") == True, 'listing_type'] = 'sale'
    df.loc[df['listing_type'].str.contains("üürile") == True, 'listing_type'] = 'rent'
    
    df['latitude'], df['longitude'] = df['geoloc'].str.split(',', 1).str
    df['longitude']=df['longitude'].astype(float)
    df['latitude']=df['latitude'].astype(float)
    
    df = df.drop('geoloc', 1)
    return df


def my_great_cleaning_function(df: object) -> object:
    df = clean_rooms(df)
    df = clean_numoffloor(df)
    df = clean_totalarea(df)
    df = clean_landarea(df)
    df = clean_price(df)
    df = clean_pricesqm(df)
    df = clean_builtyear(df)
    df = clean_energymark(df)
    df['county'] = df['county'].str.strip().str.lower()
    return df


def clean_rooms(df: object):
    df2 = df
    df2['rooms'] = df2['rooms'].str.strip().str.lower()
    mask = (df2.rooms.str.contains(
        " m²|kinnistu|-|heas|uus|vajab|:|keskmine|valmis|/|teata|kinnistu|hoonestusõigus|vundament|kaasomand|renoveeritud",
        na=False))
    df2['rooms'][mask] = np.NaN
    df2['rooms'] = pd.to_numeric(df2['rooms'], downcast='unsigned', errors='coerce')
    df2.loc[(df2.rooms < 1), 'rooms'] = np.nan
    df2.loc[(df2.rooms > 20), 'rooms'] = np.nan
    return df2


def clean_totalarea(df: object):
    df2 = df
    df2['totalarea'] = df2['totalarea'].str.strip().str.lower()
    df2['totalarea'] = df2['totalarea'].str.replace(r'm²', '')
    df2['totalarea'] = pd.to_numeric(df2['totalarea'], errors='coerce')
    return df2


def clean_landarea(df: object):
    df2 = df
    mask = (~df2.landarea.str.contains(" m²", na=False))
    df2['landarea'][mask] = np.NaN
    df2['landarea'] = df2['landarea'].str.strip().str.lower()
    df2['landarea'] = df2['landarea'].str.replace(r'm²', '')
    df2['landarea'] = pd.to_numeric(df2['landarea'], errors='coerce')
    return df2


def clean_price(df: object):
    df2 = df
    df2['price'] = df2['price'].astype('str')
    df2['price'] = df2['price'].str.replace(r'€/m2|€| ', '')
    df2['price'] = pd.to_numeric(df2['price'], errors='coerce')
    return df2


def clean_pricesqm(df: object):
    df2 = df
    df2['pricesqm'] = df2['pricesqm'].astype('str')
    df2['pricesqm'] = df2['pricesqm'].str.replace(r'€/m2|€| ', '')
    df2['pricesqm'] = pd.to_numeric(df2['pricesqm'], errors='coerce')
    return df2


def clean_numoffloor(df: object):
    df2 = df
    mask = (df2.numoffloor.str.contains(" m²", na=False))
    n = df2['numoffloor'][mask]
    df2['numoffloor'][mask] = df2['totalarea'][mask]
    df2['totalarea'][mask] = n
    return df2


def clean_builtyear(df: object):
    df2 = df
    df2['builtyear'] = pd.to_numeric(df2['builtyear'], downcast='unsigned', errors='coerce')
    df2.loc[(df2.builtyear <= 1700), 'builtyear'] = np.nan
    df2.loc[(df2.builtyear >= 2022), 'builtyear'] = np.nan
    return df2

def clean_energymark(df: object):
    df2 = df
    df2['energymark'] = df2['energymark'].astype(str).str.strip().str.lower()
    mask = (df2.energymark.str.contains("-|Puudub|nan", na=False))
    df2['energymark'][mask] = np.NaN
    return df2


def clean_condition(df: object):
    df2 = df
    df2['condition'] = df2['condition'].astype(str).str.strip().str.lower()
    df2.loc[df2['condition'].str.contains("heas korras") == True, 'condition'] = 'good_condition'
    df2.loc[df2['condition'].str.contains("uus") == True, 'condition'] = 'new'
    df2.loc[df2['condition'].str.contains("renoveeritud") == True, 'condition'] = 'renovated'
    df2.loc[df2['condition'].str.contains("vajab renoveerimist") == True, 'condition'] = 'needs_renovation'
    df2.loc[df2['condition'].str.contains("valmis") == True, 'condition'] = 'ready'
    df2.loc[df2['condition'].str.contains("san. remont tehtud") == True, 'condition'] = 'san_work_done'
    df2.loc[df2['condition'].str.contains("keskmine") == True, 'condition'] = 'moderate'
    df2.loc[df2['condition'].str.contains("vajab san. remonti") == True, 'condition'] = 'san_work_needed'
    return df2

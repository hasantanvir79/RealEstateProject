from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import datetime
import pandas as pd
import numpy as np
import os
os.chdir('/home/hasan/statistikaamet/RealEstateProject')


def algandmed(x):
    path="/home/hasan/statistikaamet/RealEstateProject"
    link_file = open(x)
    #path="C:\\Users\\TAN\\Documents\\IM\\RealEstateProject\\tmp"
    for url in link_file.read().splitlines():
        df = dataframe(url)
        dt = str(datetime.date.today())
        df.to_csv(open(path + '_' + dt + '.csv', 'w'))
        writer = pd.ExcelWriter(path + '_' + dt + '.xlsx')
        df.to_excel(writer, 'Sheet1')
        writer.save()
        print(df.head())
        print(df.tail())
        print(len(df))


def generate_links(x):

    """Parse links from a file ('links.txt')
    and add pagination (+1) to the link"""
    urls = []
    MAX_PAGE_NUM = 508
    MAX_PAGE_DIG = 1
    for i in range(1, MAX_PAGE_NUM + 1):
        page_num = (MAX_PAGE_DIG - len(str(i))) * "0" + str(i)
        url = x + page_num
        urls.append(url)
    print("\n Pages that will be scraped: \n\n", urls)
    return urls


def driver_init():

    """Select the driver and driver options"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # You need to specify the place you have your chrome/firefox etc installed
    options.binary_location = '/usr/bin/google-chrome'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    #driver = webdriver.Chrome(options=options)
    #driver.set_window_size(1120, 550)
    return driver
    print('\t Driver initialized \n',
          'Driver: %s \n' % driver,
          'Options: %s' % options)


def get_links(x):

    """Initialize lists"""
    urls = generate_links(x)
    hrefs = []

    """Scrape through list of urls"""
    for idx, url in enumerate(urls, start=1):
        driver = driver_init()
        driver.get(url)
        products = driver.find_elements_by_css_selector('.object-title-a')

        """For each url scrape all items into a list"""
        num_page_items = len(products)
        print(num_page_items)
        for i in range(num_page_items):
            try:
                href = products[i].get_attribute('href')
                hrefs.append(href)
                """Error handling for IndexError"""
            except IndexError as e:
                print("Error: %s" % e)
            else:
                print('No exceptions occured')
        driver.quit()
        print("\n Page #", idx, url)
        print("+ @href info of producs added to links")

    """Eemaldan linkide nimistust duplikaadid"""
    print(len(hrefs))
    return hrefs


def toote_info(x):

    driver = driver_init()
    links = get_links(x)

    name = []
    rooms = []
    totalarea=[]
    landarea=[]
    price = []
    pricesqm = []
    numoffloor = []
    saadavus = []
    geoloc =[]
    builtyear=[]
    energymark=[]
    condition=[]
    link = []
    
    #geoloc_elem
    latlong=[]
    for n in links:
        try:
            driver.get(n)
            print(n)
        except Exception as e:
            print("NoSuchElementException \n" + str(e))
            pass
        
        try:
            name.append(driver.find_element_by_css_selector('.large .title').text)
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            name.append(None)
        
        try:
            rooms.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[1]/td').text)
            print(rooms)
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            rooms.append(None)
        
        try:
            totalarea.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[2]/td').text)
    
            print("before: ", totalarea)     
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            totalarea.append(None)
            print("After exception: ", totalarea)

        try:
            #if (driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[1]/th').text=='Krundi pind'):
                #print("Im here ***********************")
            landarea.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[1]/td').text)
    
            #print("before: ", landarea)     
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            landarea.append(None)
            #print("After exception: ", landarea)   
        
        
        
        
        try:
            price.append(driver.find_element_by_css_selector('.m-1-2 strong').text)
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            price.append(None)
        
        try:
            pricesqm.append(driver.find_element_by_css_selector('.object-m2-price').text)
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            pricesqm.append(None)
        
        try:
            numoffloor.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[3]/td').text)
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            numoffloor.append(None)    
        
        try:
            if (driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[3]/th').text=='Ehitusaasta'):
                builtyear.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[3]/td').text)
            elif (driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[4]/th').text=='Ehitusaasta'):
                builtyear.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[4]/td').text)
            elif (driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[5]/th').text=='Ehitusaasta'):
                builtyear.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[5]/td').text)
            elif (driver.find_element_by_xpath(' /html/body/div[2]/div/div[2]/div[3]/div[1]/div/div[6]/div[1]/div/div/table[2]/tbody/tr[4]/th').text=='Ehitusaasta'):
                builtyear.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[1]/div/div[6]/div[1]/div/div/table[2]/tbody/tr[4]/td').text)
           
           
            print(builtyear)
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            builtyear.append(None)
            print("After exception: ", builtyear)

              
                
        try:
            if (driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[5]/th').text=='Seisukord'):
                condition.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[5]/td').text)            
                
            elif (driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[6]/th').text=='Seisukord'):
                condition.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[6]/td').text)
                
            elif (driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[7]/th/a').text=='Seisukord'):
                condition.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[7]/td').text)
                
            elif (driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[4]/th/a').text=='Seisukord'):
                condition.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[4]/td').text)

            elif (driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[8]/th/a').text=='Seisukord'):
                condition.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/table/tbody/tr[8]/td').text)
            elif (driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[1]/div/div[6]/div[1]/div/div/table[2]/tbody/tr[4]/th').text=='Seisukord'):
                condition.append(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/div[1]/div/div[6]/div[1]/div/div/table[2]/tbody/tr[4]/td').text)
              
                 
            
            
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            condition.append(None) 
        
        try:
            geoloc.append(driver.find_element_by_xpath('//*[@id="gmap_img"]/a').get_attribute('href').split('&query=')[1])
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            geoloc.append(None)
        
        try:
            link.append(n)
        except Exception as e:
            print("Exception \n" + str(e))
            link.append(None)
            
            
            
            
        
        try:
            energymark.append(driver.find_element_by_css_selector('.energy-label').text)
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            energymark.append(None)
             
           
        except NoSuchElementException as e:
            print("NoSuchElementException \n" + str(e))
            energymark.append(None)  

        


    """Quit the driver to save memory"""
    driver.quit()
    print(name, rooms, price, saadavus)

    """Zip all the lists into a table"""
    data = [{'name': t_name,
             'rooms': t_rooms,
             'totalarea': t_totalarea,
             'landarea':t_landarea,
             'price': t_price,
             'pricesqm': t_pricesqm,
             'numoffloor': t_numoffloor,
             'geoloc': t_geoloc,
             'builtyear': t_builtyear,
             'energymark': t_energymark,
             'condition': t_condition,
             'link': t_link} for t_name, t_rooms, t_totalarea, t_landarea,
            t_price, t_pricesqm, t_numoffloor, t_geoloc, t_builtyear, t_energymark, t_condition, t_link, in zip(name, rooms, totalarea, landarea, price, pricesqm, numoffloor, geoloc, builtyear, energymark, condition, link)]
    print(data)

    return data


def dataframe(x):
    df = pd.DataFrame(toote_info(x))
    date = pd.to_datetime('today').strftime('%Y-%m-%d')
    df['date'] = date
    df.replace('', np.nan, inplace=True)
    columns = ['date', 'name', 'rooms', 'totalarea', 'landarea', 'price', 'pricesqm', 'numoffloor', 'geoloc' , 'builtyear', 'energymark', 'condition', 'link']
    df = df.reindex(columns=columns)
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    '''Filter out data from dataframe'''
    columns = ['date', 'name', 'rooms', 'totalarea', 'landarea', 'price', 'pricesqm', 'numoffloor', 'geoloc' , 'builtyear', 'energymark', 'condition', 'link']
    df = df.reindex(columns=columns)
    #df.drop_duplicates(subset=None, keep='first', inplace=True)
    '''How many missing values are in the dataframe'''
    nans = df.isnull().sum().sum()
    nan_rows = df.isnull().sum()
    if nans > 0:
        print('Sum of missing values', nans, '\n',
              'missing values per category \n', nan_rows)
    else:
        print('No missing values in dataframe')
    return df


if __name__ == '__main__':
    algandmed('links.txt')

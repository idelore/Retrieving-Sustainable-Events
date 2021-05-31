# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 11:09:44 2019

@author: Ignacio de Lorenzo
"""

import pandas as pd
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")
#from googlesearch import search 
from selenium import webdriver
import os
import time as time
import datetime



driver = webdriver.Chrome()

fecha=datetime.datetime(2020,2,25, 10, 15, 00, 00000)

title=[]
id=[]

for d in range(0,465):
 
    time.sleep(1)
    fecha=fecha+datetime.timedelta(days=1) 
    print(fecha)   
    origen="https://www.trumba.com/calendars/gazette?date=0000000000&filterview=Gazette+Classification&filter1=_1658005_41129_67204_41149_41130_41156_41140_41141_41131_41142_78368_41132_41133_41143_41144_41134_41135_41136_41155_67253_67883_41145_41137_41159_79205_41138_41139_41150_41160_229262_41147_41157_41158_64137_&filterfield1=15202&media=print"
    web=origen.replace("0000000000",str(fecha.year)+str(fecha.month).zfill(2)+str(fecha.day).zfill(2))
    driver.get(web)
    soup=BeautifulSoup(driver.page_source, 'html') 
    
    events=soup.find_all(class_="ebg0")
  
    for e in events:
        e=e.find_all(class_="ebg0")
        if len(e)>2:
            id.append(e[2].find("a")["eventid"])
            title.append(e[2].find("a")["url.seotitle"])
    
results=pd.DataFrame(zip(id,title), columns=['Id', 'title'])
results.to_excel("ids de Harvard.xlsx",sheet_name='Harvard')
results=pd.read_excel("ids de Harvard.xlsx",sheet_name='Harvard')
results.drop_duplicates(subset="Id",
                                keep = False, 
                                inplace = True)
results["title2"]=""
results["descrip"]=""
results["web"]=""
results["date"]=""

for i in range(0,len(results)):
    results.copy()
    time.sleep(1)
    idevent=results.iloc[i]["Id"]
    origen="https://www.trumba.com/calendars/gazette?filterview=Gazette+Classification&filter1=_41129_67204_41149_41130_41156_41140_41141_41131_41142_78368_41132_41133_41143_41144_41134_41135_41136_41155_67253_67883_41145_41137_41159_79205_41138_41139_41150_41160_229262_41147_41157_41158_64137_&filterfield1=15202&eventid=000000000000&view=event&media=print"
    web=origen.replace("000000000000",str(idevent))
    driver.get(web)
    soup=BeautifulSoup(driver.page_source, 'html')
    tbl=soup.find("table")
    results.iloc[i, results.columns.get_loc('web')] = web
    results.iloc[i, results.columns.get_loc('title2')] = soup.find(class_="twEDDescription").text
    print(soup.find(class_="twEDDescription").text)
   
    for tr in tbl.find_all('tr'):        
       for td in tr.find_all('th'):
           if td.text=="Details":               
               bloque=tr.find_all("td")
               for b in bloque:
                   results.iloc[i, results.columns.get_loc('description')] = b.text
           if td.text=="When":               
               bloque=tr.find_all("td")
               for b in bloque:
                   results.iloc[i, results.columns.get_loc('date')] = b.text
        
results.to_excel("eventos de Harvard.xlsx",sheet_name='Harvard')  

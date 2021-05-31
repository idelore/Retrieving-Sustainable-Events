# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 11:09:44 2019

@author: Ignacio de Lorenzo
"""


import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import re, string
#from googlesearch import search 

resultadolen=0
positivos=0

palabrasclaves = pd.read_excel('keywordsods.xlsx', sheet_name='Tabla')
eventos=pd.read_excel('eventos de Harvard.xlsx', sheet_name='Harvard')
resultado= eventos.copy(deep=True)
odsp=[ ]

sdgall=list(pd.unique(palabrasclaves['SDG']))

def palabreador (text):
    text=re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text=text.lower()
    text = " ".join(text.split())
    return text

for sdg in sdgall:
    odsp=[]
    pods=list(palabrasclaves[palabrasclaves['SDG']==sdg]["Key"])
    podslen=len(pods)
    # Iteración por filas del DataFrame:
    for indice_fila, fila in eventos.iterrows():
        positivos=0
        desc=palabreador(fila["descrip"])
        for palabra in pods:
            palabra=palabra.lower()
            if desc.find(" " + palabra + " ")!=-1:
                positivos=positivos + 1
        ppositivos=positivos
        odsp[len(odsp):] = [ppositivos]
    resultado[sdg]=odsp
    print("---------------------")
    print(pods)
    print(ppositivos)
    
resultadopos=eventos.copy(deep=True)

umbral=0.05

for sdg in sdgall:
    odsp=[]
    pods=list(palabrasclaves[palabrasclaves['SDG']==sdg]["Key"])
    podslen=len(pods)
    print(sdg)
    for indice_fila, fila in resultado.iterrows():
        print("---------->" + str(indice_fila))
        print (fila[sdg])
        poractivo=fila[sdg]/podslen
        print(poractivo)
        if poractivo>umbral:
            resultadopos.loc[indice_fila,sdg]=1
            print("Positivo")
        else:
            resultadopos.loc[indice_fila,sdg]=0
            print("Negativo")


resultadopor=resultado.copy(deep=True)

for sdg in sdgall:
    odsp=[]
    pods=list(palabrasclaves[palabrasclaves['SDG']==sdg]["Key"])
    podslen=len(pods)
    print(sdg)
    for indice_fila, fila in resultado.iterrows():
        print(indice_fila)
        poractivo=(fila[sdg]/podslen)*10
        print(poractivo)
        resultadopor.loc[indice_fila,sdg]=poractivo
        
        
resultadopalabras=eventos.copy(deep=True)

for sdg in sdgall:
    pods=list(palabrasclaves[palabrasclaves['SDG']==sdg]["Key"])
    podslen=len(pods)
    # Iteración por filas del DataFrame:
    for palabra in pods:
        odsp=[]
        palabra=palabra.lower()
        positivos=0
        for indice_fila, fila in eventos.iterrows():
            desc=palabreador(fila["descrip"])
            desc=str(desc).lower()
            if desc.find(" " + palabra + " ")!=-1:
                positivos=desc.count(" " + palabra + " ")
            ppositivos=positivos
            odsp[len(odsp):] = [ppositivos]
        nomsdg=str(sdg)+"-"+ str(palabra)
        resultadopalabras[nomsdg]=odsp
    print("---------------------")
    

with pd.ExcelWriter('analisis eventos ODS Harvard.xlsx') as writer: 
    resultado.to_excel(writer, sheet_name='Número de palabras')
    resultadopos.to_excel(writer, sheet_name='Porcentaje umbral ' + str(umbral))  
    resultadopor.to_excel(writer, sheet_name='Porcentaje')
    resultadopalabras.to_excel(writer, sheet_name='Palabras') 

resultadobuscador=pd.melt(resultado,value_vars=['SDG 01', 'SDG 02', 'SDG 03', 'SDG 04', 'SDG 05', 'SDG 06', 'SDG 07',
       'SDG 08', 'SDG 09', 'SDG 10', 'SDG 11', 'SDG 12', 'SDG 13', 'SDG 14',
       'SDG 15', 'SDG 16', 'SDG 17'],id_vars=['Id', 'title', 'title2', 'descrip', 'web', 'date'])

resultadobuscador.to_excel("buscador Harvard.xlsx", sheet_name='Número de palabras')
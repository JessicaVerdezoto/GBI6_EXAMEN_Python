 
import Bio 
from Bio import Entrez
import re
import pandas as pd
import csv
import itertools
import numpy as np
def download_pubmed(keyword: str):
    """La primera función download_pubmed se usa para extraer el conteo
     de los IDs de los artículos con una palabra clave -keyword- definida respectivamente"""
    Entrez.email = "jessica.verdezoto@est.ikiam.edu.ec"
    hand = Entrez.esearch(db="pubmed",
                        retmax=1000000,
                        retmode='xml',
                        term=keyword)
    dat = Entrez.read(hand)                    
    hand.close()
    return dat

def mining_pubs(tipo: str) -> pd.DataFrame :
    """La segunda función mining_pubs se usa para extraer datos mas precisos ubicados en el texto, utilizando otros parametros, en este caso usamos -tipo-"""
    """
    Si el tipo es "DP" proporciona el año de publicación de el artículo. Retorna como un dataframe con el -PMID- y el -DP_year-.
    Si el tipo es "AU" proporciona el número de autores por PMID. Retorna como un dataframe con el -PMID- y el -num_auth-. 
    Si el tipo es "AD" proporcion el conteo de autores por país. El retorno es un dataframe con el -country- y el -num_auth-.
    """
    info =download_pubmed ('Ecuador genomics') 

    res_iD = info['IdList'] #Se obtiene los IDs
    ids = ','.join(res_iD)
    Entrez.email = "jessica.verdezoto@est.ikiam.edu.ec"
    hand = Entrez.efetch(db="pubmed",
                        rettype='medline',
                        retmode='text',
                        id=ids)
    datos = hand.read()  

    if (tipo == "DP"): #Primer literal PMID Y DP_year

        zipcodes = re.findall(r'PMID-.(.+)', datos) #Para el ID de cada artículo
        zipcodes1 = re.findall(r'DP  -.(\d+)', datos) #Para el año de publicación de los artículos
        zipcodes1 = [int(i) for i in zipcodes1]  
        allDat = list(zip(zipcodes,zipcodes1))
        nom_colum = ['PMID','DP_year']
    else:
        if(tipo == "AU"): #Segundo literal PMID Y num_auth
            zipcodes = re.findall(r'PMID-.(.+)|(AU)  -|', datos) 
            nom_colum = ['PMID','num_auth']
            
        elif(tipo == "AD"):#Tercer literal country y el num_auth
            zipcodes = re.findall(r'PL  -.(.+)|(AU)  -|', datos)
            nom_colum = ['country','num_auth']
            
        allDat = list()
        for x in zipcodes:
            if(x[0]!=''):
                allDat.append((x[0],''))
            elif(x[1]!=''):
                allDat.append(('',x[1]))

        zipcodes = allDat       
        list1 = list()
        list2 = list()
        va_c = 0
        for y in zipcodes:
            if(y[0] !=''):
                x_0 = y[0]
                list1.append(y[0])
                if(va_c != 0):
                    list2.append(va_c)
                    va_c = 0
            else:
                va_c = va_c+1          
        allDat = list(zip(list1,list2))
        
    hand.close()
    info = pd.DataFrame(allDat, columns=nom_colum) 
    return info


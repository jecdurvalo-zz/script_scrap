
# coding: utf-8

# In[11]:


import requests
import json
import re
import pandas as pd
import numpy as np
import xlsxwriter
import datetime


# In[12]:

# Captura os itens direto da API
def item_api(item,offset,token):
    r = requests.get("https://api.mercadolibre.com/sites/MLB/search?q={}&offset={}&access_token={}".format(item.replace(" ","%20"),offset,token))
    r = json.loads(r.text)
    r = r["results"]
    return r

# Define o numero de anuncios da busca para ser usado no offset da API
def limite(item,token):
    r = requests.get("https://api.mercadolibre.com/sites/MLB/search?q={}&offset=0&access_token={}".format(item.replace(" ","%20"),token))
    r = json.loads(r.text)
    r = r["paging"]
    r = r["total"]
    return r
# Pega os dados do vendedor (não esta sendo usado)
def api_seller(seller_id,token):
    r = requests.get('https://api.mercadolibre.com/users/{}?access_token={}'.format(seller_id,token))
    r = json.loads(r.text)
    return r

# Transforma a variavel em Dataframe do Panda e Renomeia
def df_renomea(df):
    df = pd.DataFrame(df)    
    df = df.rename(columns={0: "filtro",1:"seller",2:"item_id",3:"title",4:"price",5:"stop_time",6:"condition"})
    return df


# In[13]:

#Data atual para gerar o arquivo
data_atual_file = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
token = "ADM-601-111912-01ea7e53e867bea5a28584a1930a1b60-jecdurvalo-62867623"


# In[ ]:


contador = 0
t = 0
f = 0
maximo = 0

resultado = []
# Lista dos itens e valores minimos e maximos buscados pelo script
lista_itens = pd.read_csv("C://Users//jecdurvalo//Documents//Rose//itens_monitoramento.csv")
lista = []
valor_min = []
valor_max = []
# Junsta a info em uma unica lista
fraude = pd.DataFrame(columns=['filtro','seller','item_id','title','price'])
for i in lista_itens["item"]:
    lista.append(i)

for i in lista_itens["min"]:
    valor_min.append(i)
    
for i in lista_itens["max"]:
    valor_max.append(i)

#Cria o primeiro Dataframe com a informação de todos os anuncios.
while t < len(lista):
    maximo =  limite(lista[t],token)
    while contador < maximo:
        api_resultado = item_api(lista[t],contador,token)
        for i in api_resultado:
            resultado.append([lista[t],i["seller"]["id"],i["id"],i["title"],i["price"],i['stop_time'],i['condition']])        
        contador += 50        
    t += 1    
    contador = 0  
else:
    resultado = df_renomea(resultado)

fraude = pd.DataFrame(columns=['filtro','seller','item_id','title','price'])

# Faz o filtro por valor e numero de anuncios
while f < len(lista_itens):
    r = resultado[(resultado["filtro"] == lista_itens["item"][f]) & (resultado["price"] > lista_itens["min"][f]) & (resultado["price"] < lista_itens["max"][f])] 
    fraude = fraude.append(r)
    f += 1  
    
fraude = fraude 
# apaga dos duplicados
fraude = fraude.drop_duplicates("seller", keep='last')

# salva o arquivo
writer = pd.ExcelWriter('C://Users//jecdurvalo//Documents//Rose//items-black-rose-{}.xlsx'.format(data_atual_file))
fraude.to_excel(writer, 'Planilha1') 
writer.save()


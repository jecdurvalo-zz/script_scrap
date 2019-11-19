
# coding: utf-8

# In[23]:


import requests
import pandas as pd
import numpy as np
import json
import datetime


# In[24]:


token = 'ADM-601-112218-bd9b1e86b3afce9d86f09e1da4e99e08-fbsampaio-62867623'


# In[25]:

# Pega os dados do vendedor
def api_seller(seller_id,token):
    r = requests.get('https://api.mercadolibre.com/users/{}?access_token={}'.format(seller_id,token))
    r = json.loads(r.text)
    return r

# cria os Dataframe do panda e renomeia as colunas
def df_renomea(df):
    df = pd.DataFrame(df)    
    df = df.rename(columns={0: "seller", 1:"dt_created"})
    return df


# In[26]:

# datas atuais
data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
data_atual_file = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# Pega a informação do NOC
noc = requests.get("http://noc.ml.com/v2/api/list/collector_id?marketplace=MELI&date_from={}&date_to={}&site_id=MLB".format(data_atual,data_atual))
noc = json.loads(noc.text)


# In[27]:


i = 0
t = 0
noc_s = []
s = []
seller = []

for z in noc:
    noc_s.append(z['cust_id'])
while i < len(noc_s):
    s.append(api_seller(noc_s[i],token))
    i += 1
else:
    i = 0

while t < len(s):
    seller.append([s[t]['id'],s[t]['registration_date']])
    t += 1
    
seller = df_renomea(seller)
seller = seller[seller["dt_created"] > '2018-09-01'].sort_values(by="dt_created", ascending=False)


writer = pd.ExcelWriter('G://Meu Drive//Black Friday//noc-{}.xlsx'.format(data_atual_file))
seller.to_excel(writer, 'Sheet1')
writer.save()


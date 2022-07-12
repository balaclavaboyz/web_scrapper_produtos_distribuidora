import requests
from bs4 import BeautifulSoup

with open('res.html','r') as f:
    data= f.read()

soup=BeautifulSoup(data,features="html.parser")

productlist=soup.find_all('span',class_='price')

productlinks=[]

for i in productlist:
    for link in i.find_all('a',href=True):
        productlinks.append(link['href'])

# print(len(productlinks))
# print(productlist)
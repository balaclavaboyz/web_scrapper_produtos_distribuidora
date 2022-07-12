import grequests
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import sqlite3
from pandas.core.frame import DataFrame
import psycopg2
from sqlalchemy import create_engine
import selenium
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from pandas.io.json import json_normalize



def fujioka_gerar_html_page():
    # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    s = Service(GeckoDriverManager().install())
    # browser = webdriver.Firefox(executable_path="./geckodriver.exe")
    # browser.get("https://app.finxter.com/")
    options = webdriver.FirefoxOptions()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    options.headless = True

    driver = webdriver.Firefox(options=options, service=s)

    driver.get('https://www.fujiokadistribuidor.com.br/')

    search = driver.find_element_by_xpath(
        '/html/body/header/div[2]/div/div/div[2]/ul/li[2]/p/em/a')

    search.click()

    login = driver.find_element_by_xpath('//*[@id="loginInputEmailCL"]')

    login.send_keys('milvestcontato@gmail.com')
    login.send_keys(Keys.ENTER)

    sleep(10)

    entrar = driver.find_element_by_xpath(
        '//*[@id="loginWithUserAndPasswordBtn"]')
    entrar.click()

    sleep(10)

    senha = driver.find_element_by_xpath('//*[@id="inputPassword"]')
    senha.send_keys('ema|Aq0x%=I:)I`ZKA#~')
    senha.send_keys(Keys.ENTER)

    sleep(10)

    headers=driver.execute_script("fetch()")
    headers = headers.splitlines()
    print(headers)

    with open('headers.json','w') as f:
        json.dump(headers,f)
    driver.close()
    return


def criar_db_fujioka_com_ml(primeira_pagina, ultima_pagina):

    db=sqlite3.connect('bomdia.sqlite')
    db.execute("PRAGMA foreign_keys=1")
    c=db.cursor()
    
    # eh necessario ter headers se nao eh possivel realizar os requests
    headers = {
        'authority': 'www.fujiokadistribuidor.com.br',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Microsoft Edge";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'accept': 'text/html, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.38',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.fujiokadistribuidor.com.br/informatica',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '_gcl_au=1.1.683158933.1635476952; VtexRCMacIdv7=ed9b8361-cd15-4466-a23d-ad52dd96453e; _fbp=fb.2.1635476952984.1022983344; blueID=84c5c9fe-f7d6-4697-9aac-a7626102f258; checkout.vtex.com=__ofid=ecf7d65b29734e47acaf0a7b66c40684; .ASPXAUTH=4BDE945AEC5D0BCC6BC19E2F70292FA2C6B4F137830116551D7E0A3F4AB07D720AA51676AAD149F4383F1AC50F9180E652575945E9AFE7B21528420689C29DEF1CFDAF47189E812C190DDB3C62813B303913BF8A2BF1CBE4C0BC3CFA4AD2AC084A4CC472442726F0E55361AEE52684B00590DFA29DEE41153DCB249ED3426780900DB98A9D202A2C81F63FB428CFCE0587314A749B8B68CFD16CE9955548ABBE162A632D; nav_id=07172694-84ff-4ffa-8803-dcd8673df942; _hjid=2bf0b460-b4a6-4e04-8b78-2427ed8cdb31; legacy_p=07172694-84ff-4ffa-8803-dcd8673df942; chaordic_browserId=07172694-84ff-4ffa-8803-dcd8673df942; legacy_c=07172694-84ff-4ffa-8803-dcd8673df942; legacy_s=07172694-84ff-4ffa-8803-dcd8673df942; __bid=b2e93eca-7271-4c68-a10a-5db98ff82964; tt.u=0100007FBA657B61B60661BA02DEE237; voxusmediamanager_acs=true; _ga=GA1.1.1600606828.1635476953; _spl_pv=2; _ttuu.s=1635476986855; _ga_KRSKYCLYL9=GS1.1.1635476952.1.1.1635477034.0; i18next=pt-BR; VtexIdclientAutCookie_fujiokadistribuidor=eyJhbGciOiJFUzI1NiIsImtpZCI6IjU0MUUzMDU5ODdENEQ5MjE0Q0Y2ODM4NUM0RkI5M0QwMEMwRTg0OTciLCJ0eXAiOiJqd3QifQ.eyJzdWIiOiJtaWx2ZXN0Y29udGF0byswMzg5Nzc5MjAwMDEzN0BnbWFpbC5jb20iLCJhY2NvdW50IjoiZnVqaW9rYWRpc3RyaWJ1aWRvciIsImF1ZGllbmNlIjoid2Vic3RvcmUiLCJzZXNzIjoiMWMwN2JkMDItNTliNi00ODIyLWIyZTMtNjYxYjZkYTE0OGJhIiwiZXhwIjoxNjM1NzE2MDQ2LCJ1c2VySWQiOiIyYzAzMjhjZC02ZjBiLTQwNjYtOGY4Ni04YjZmZDg4MzVlMDciLCJpYXQiOjE2MzU2Mjk2NDYsImlzcyI6InRva2VuLWVtaXR0ZXIiLCJqdGkiOiJlZmRjOGM5OS0xYjBmLTQ0ZjgtOWQ4NC1iODdhMzYxMTUzMzkifQ.cJq_Kbdr-So96meaSxEbPupuWafxP6M_JLSf5Wea3mL_vLY5_mUjHFl6ZpxlH7LCMRRhw21xi1VT9wsJu3mA3A; VtexIdclientAutCookie_4a52d56b-bab5-406e-b928-959a7988a95f=eyJhbGciOiJFUzI1NiIsImtpZCI6IjU0MUUzMDU5ODdENEQ5MjE0Q0Y2ODM4NUM0RkI5M0QwMEMwRTg0OTciLCJ0eXAiOiJqd3QifQ.eyJzdWIiOiJtaWx2ZXN0Y29udGF0byswMzg5Nzc5MjAwMDEzN0BnbWFpbC5jb20iLCJhY2NvdW50IjoiZnVqaW9rYWRpc3RyaWJ1aWRvciIsImF1ZGllbmNlIjoid2Vic3RvcmUiLCJzZXNzIjoiMWMwN2JkMDItNTliNi00ODIyLWIyZTMtNjYxYjZkYTE0OGJhIiwiZXhwIjoxNjM1NzE2MDQ2LCJ1c2VySWQiOiIyYzAzMjhjZC02ZjBiLTQwNjYtOGY4Ni04YjZmZDg4MzVlMDciLCJpYXQiOjE2MzU2Mjk2NDYsImlzcyI6InRva2VuLWVtaXR0ZXIiLCJqdGkiOiJlZmRjOGM5OS0xYjBmLTQ0ZjgtOWQ4NC1iODdhMzYxMTUzMzkifQ.cJq_Kbdr-So96meaSxEbPupuWafxP6M_JLSf5Wea3mL_vLY5_mUjHFl6ZpxlH7LCMRRhw21xi1VT9wsJu3mA3A; vtex_segment=eyJjYW1wYWlnbnMiOm51bGwsImNoYW5uZWwiOiIxIiwicHJpY2VUYWJsZXMiOiJVRkRTUC1MVDMzLUNUMDEtU1UwMC1ERTAwLVNJMDAtQ1MwMSIsInJlZ2lvbklkIjpudWxsLCJ1dG1fY2FtcGFpZ24iOm51bGwsInV0bV9zb3VyY2UiOm51bGwsInV0bWlfY2FtcGFpZ24iOm51bGwsImN1cnJlbmN5Q29kZSI6IkJSTCIsImN1cnJlbmN5U3ltYm9sIjoiUiQiLCJjb3VudHJ5Q29kZSI6IkJSQSIsImN1bHR1cmVJbmZvIjoicHQtQlIiLCJhZG1pbl9jdWx0dXJlSW5mbyI6InB0LUJSIiwiY2hhbm5lbFByaXZhY3kiOiJwdWJsaWMifQ; VTEXSC=sc=1; ISSMB=ScreenMedia=0&UserAcceptMobile=False; IPI=UsuarioGUID=2c0328cd-6f0b-4066-8f86-8b6fd8835e07; vtex_session=eyJhbGciOiJFUzI1NiIsImtpZCI6IkMwMDUzNDVBMkM5MTFGRUFFMzQzOUNBNUMxNDZCNTYwNjdEODQxM0UiLCJ0eXAiOiJqd3QifQ.eyJhY2NvdW50LmlkIjoiNGE1MmQ1NmItYmFiNS00MDZlLWI5MjgtOTU5YTc5ODhhOTVmIiwiaWQiOiJkNjM0YjYyOC03ZTQ3LTQ1ODEtYjkyZC1iYzI5MjNmMWJhMTgiLCJ2ZXJzaW9uIjo0LCJzdWIiOiJzZXNzaW9uIiwiYWNjb3VudCI6InNlc3Npb24iLCJleHAiOjE2MzYzMjA4NDgsImlhdCI6MTYzNTYyOTY0OCwiaXNzIjoidG9rZW4tZW1pdHRlciIsImp0aSI6IjViYjc3NGFhLWFkN2QtNDFhOC1hMWI0LWY2YzA1Yjc2MDVlMyJ9.SMjfP8JyqLo7-VQHbOwCK4jwYCLttufcElK9YZl3KHxAWrBdKQRTIvBKaSuB0VhXMjpZzrpU9TsnecRgoXgrCw; janus_sid=93eb58a0-3bbb-452c-b7d6-3e9bdc06b6b9; SGTP=UGUIDReturn=True; SGTS=6C83EE5EC362FF6BE9DBABEDF0B9570C; urlLastSearch=http://www.fujiokadistribuidor.com.br/informatica'
    }

    # criar uma lista de links antes para mandar tudo no grequests para paralelizacao
    lista_de_links_pregerado = []

    for x in range(primeira_pagina, ultima_pagina+1):
        lista_de_links_pregerado.append(
            f'https://www.fujiokadistribuidor.com.br/buscapagina?fq=C%3a%2f11%2f&PS=32&sl=e26b41c8-257e-4456-9760-9217930ec898&cc=32&sm=0&PageNumber={x}')
        print(f'Gerando lista de links: {x} de {ultima_pagina}')
    print('Mandando requests para todos os links')
    resp = grequests.map([grequests.get(i, headers=headers)
                         for i in lista_de_links_pregerado])
    print('Done links')

    # sql init
    c.executescript('''
        DROP TABLE IF EXISTS produto;
        DROP TABLE IF EXISTS price;
        DROP TABLE IF EXISTS link;
        DROP TABLE IF EXISTS nome;
    ''')
    c.execute('''
        DROP TABLE IF EXISTS pesquisa;
    ''') 
    c.execute('''
        CREATE TABLE IF NOT EXISTS price(
            priceid INTEGER PRIMARY KEY,
            priceml BLOB,
            pricefuj TEXT 
        ) 
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS link(
            linkid INTEGER PRIMARY KEY,
            linkml TEXT,
            linkfuj TEXT 
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS nome(
            nomeid INTEGER PRIMARY KEY,
            nomeml TEXT,
            nomefuj TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS produto(
            produtoid INTEGER PRIMARY KEY,
            linkid INTEGER,
            priceid INTEGER,
            nomeid INTEGER,
            FOREIGN KEY (linkid) REFERENCES link (linkid),
            FOREIGN KEY (priceid) REFERENCES price(priceid),
            FOREIGN KEY (nomeid) REFERENCES nome(nomeid)
        )
    ''')

    # aqui acontece o parse
    for r in resp:
        soup = BeautifulSoup(r.content, features="html.parser")
        productList = soup.find_all('span', class_='price')

        for bloco_de_span in productList:
            nomefuj = ''
            for item in bloco_de_span.find_all('a', href=True):
                enderecofuj = item['href']
                nomefuj = item['title']

                try:
                    try:
                        por = item.text.split()[5]
                    except:
                        por = '0' 

                except:
                    print('Saiu do if por causa do NoneType')

                print('Enviando request para mercadolivre: '+nomefuj)

                c.execute("DROP TABLE IF EXISTS produtomercadolivre;")
                c.execute('''CREATE TABLE produtomercadolivre(
                        "id" TEXT,
                        "official_store" TEXT,
                        "bookmarked" BOOL,
                        "discount_source" TEXT,
                        "seller_info" TEXT,
                        "permalink" TEXT,
                        "pictures" TEXT,
                        "price" TEXT,
                        "title" TEXT,
                        "subtitles" TEXT,
                        "vertical" TEXT,
                        "is_ad" BOOL,
                        "installments" TEXT,
                        "tags" TEXT,
                        "image_ratio" REAL,
                        "category_id" TEXT,
                        "pictures_quantity" INTEGER,
                        "rebates" TEXT,
                        "vertical_highlight" TEXT,
                        "value_propositions" TEXT,
                        "available_quantity" INTEGER,
                        "shipping" TEXT,
                        "ad_label" TEXT,
                        "ad_version" TEXT,
                        "product" TEXT,
                        "reviews" TEXT,
                        "highlight" TEXT,
                        "details" TEXT,
                        "item_highlight" TEXT,
                        "variations_picker" TEXT,
                        "variations" TEXT
                    )''')

                df_produtos = pd.DataFrame()
                temp_df=pd.DataFrame()


                z= requests.get(f'https://lista.mercadolivre.com.br/{nomefuj}')
                soup = BeautifulSoup(z.content, features="html.parser")
                scripts_tags = soup.find_all('script')
                result = None

                for q in scripts_tags:
                    search = re.search(
                        "window.__PRELOADED_STATE__ =\n     (.+);", q.text)
                    if search != None:
                        result = search
                        break
                try:
                    if result.group(1) != None:
                        print('Lista de produto encontrado')
                        dump = json.loads(result.group(1))
                        temp_df= pd.DataFrame(dump['initialState']['results'])
                        
                        # name = dump['initialState']['results'][0]['title']
                        # df_produtos = pd.concat([df_produtos, temp_df])
                except:
                    print('! N achou lista de produto')

                # vou querer que todos os link e precos e nomes aparecem em cada entrada de fuj

                json_price_ml=[]
                json_link_ml=[]
                json_nome_ml=[]

                for index,row in temp_df.iterrows():
                    try:
                        json_price_ml.append(int(row['price']['amount']))
                    except:
                        json_price_ml.append('0')
                    # aqui foi comentado, pq n preciso de uma lista de links do mercadolivre para verificar se realmente o item existe, pq de qualquer jeito vou precisar verificar no manual
                    # json_link_ml.append(row['permalink'])
                    json_nome_ml.append(row['title'])
                json_link_ml.append(f'https://lista.mercadolivre.com.br/{nomefuj}')
                c.execute('''
                    CREATE VIRTUAL TABLE IF NOT EXISTS pesquisa USING FTS5(nomeml,nomefuj,linkml,linkfuj,priceml,pricefuj)
                ''')
                c.execute('''
                    INSERT INTO pesquisa(nomeml,nomefuj,linkml,linkfuj,priceml,pricefuj)
                    VALUES(?,?,?,?,?,?)
                ''',(json.dumps(json_nome_ml),nomefuj,json.dumps(json_link_ml),enderecofuj,json.dumps(json_price_ml),por))
# isso aqui deu certo
                    # c.execute('''
                    #     INSERT INTO price(priceml,pricefuj)
                    #     VALUES (?,?)
                    # ''',(json.dumps(json_price_ml),por))
                    # priceid=c.execute('''
                    #     SELECT last_insert_rowid()
                    # ''')
                    # # print(temp.lastrowid)
                    # c.execute('''
                    #     INSERT INTO link(linkml,linkfuj)
                    #     VALUES (?,?)
                    # ''',(json.dumps(json_link_ml),enderecofuj))
                    # linkid=c.execute('''
                    #     SELECT last_insert_rowid()
                    # ''')

                    # c.execute('''
                    #     INSERT INTO nome(nomeml,nomefuj)
                    #     VALUES (?,?)
                    # ''',(json.dumps(json_nome_ml),nomefuj))
                    # nomeid=c.execute('''
                    #     SELECT last_insert_rowid()
                    # ''')

                    # c.execute('''
                    #     INSERT INTO produto(priceid,linkid,nomeid)
                    #     VALUES (?,?,?)
                    # ''',(priceid.lastrowid,linkid.lastrowid,nomeid.lastrowid))
                # for index,row in temp_df.iterrows():

                #     c.execute('''
                #         INSERT INTO price(priceml,pricefuj)
                #         VALUES (?,?)
                #     ''',(json.dumps(row['price']),por))
                #     priceid=c.execute('''
                #         SELECT last_insert_rowid()
                #     ''')
                #     # print(temp.lastrowid)
                #     c.execute('''
                #         INSERT INTO link(linkml,linkfuj)
                #         VALUES (?,?)
                #     ''',(row['permalink'],enderecofuj))
                #     linkid=c.execute('''
                #         SELECT last_insert_rowid()
                #     ''')

                #     c.execute('''
                #         INSERT INTO nome(nomeml,nomefuj)
                #         VALUES (?,?)
                #     ''',(row['title'],nomefuj))
                #     nomeid=c.execute('''
                #         SELECT last_insert_rowid()
                #     ''')

                #     c.execute('''
                #         INSERT INTO produto(priceid,linkid,nomeid)
                #         VALUES (?,?,?)
                #     ''',(priceid.lastrowid,linkid.lastrowid,nomeid.lastrowid))

                    
                # df_produtos.to_csv('tmp', index=False)
                # aux = pd.read_csv('tmp')
                # aux.to_sql('mercadolivre', db, if_exists='replace', index=False)

                # produto = {
                #     'nome': nomefuj,
                #     'por': por,
                #     'link': enderecofuj
                # }

                # # juntar todos os prod em DF
                # print('Salvando: ', produto['nome'])
                # produtoLista.append(produto)



    # # # dps de ter terminado a lista de produtos da fujioka, eh salvo em um DF e dps para banco de dados
    # # df_fuj = pd.DataFrame(produtoLista)

    # # df_fuj.to_sql('fujioka', db, if_exists='replace', index=True)
    # # gerar_db()
    # df_ml=pd.read_sql('select * from mercadolivre',db)

    # # APAGAR DPS
    # df_fuj=pd.read_sql('select * from fujioka',db)

    # # parser funj
    # c.execute('''
    #     DROP TABLE IF EXISTS price;
    # ''')
    # c.execute('''
    #     DROP TABLE IF EXISTS link;
    # ''')
    # c.execute('''
    #     DROP TABLE IF EXISTS nome;
    # ''')
    # c.execute('''
    #     DROP TABLE IF EXISTS produto;
    # ''')
    # c.execute('''
    #     CREATE TABLE IF NOT EXISTS price(
    #         priceid INTEGER PRIMARY KEY,
    #         priceml TEXT,
    #         pricefuj TEXT 
    #     ) 
    # ''')
    # c.execute('''
    #     CREATE TABLE IF NOT EXISTS link(
    #         linkid INTEGER PRIMARY KEY,
    #         linkml TEXT,
    #         linkfuj TEXT 
    #     )
    # ''')
    # c.execute('''
    #     CREATE TABLE IF NOT EXISTS nome(
    #         nomeid INTEGER PRIMARY KEY,
    #         nomeml TEXT,
    #         nomefuj TEXT
    #     )
    # ''')
    # c.execute('''
    #     CREATE TABLE IF NOT EXISTS produto(
    #         produtoid INTEGER PRIMARY KEY,
    #         linkid INTEGER,
    #         priceid INTEGER,
    #         nomeid INTEGER,
    #         FOREIGN KEY (linkid) REFERENCES link (linkid),
    #         FOREIGN KEY (priceid) REFERENCES price(priceid),
    #         FOREIGN KEY (nomeid) REFERENCES nome(nomeid)
    #     )
    # ''')

    # # print(df_fuj)
    # # print(df_ml)
    # priceml=[]
    # linkml=[]
    # titleml=[]

    # for index,row in df_ml.iterrows():
    #     priceml.append(json.dumps(row['price']))
    #     linkml.append(row['permalink'])
    #     titleml.append(row['title'])

    # pricefuj=[]
    # linkfuj=[]
    # nomefuj=[]

    # for index,row in df_fuj.iterrows():
    #     pricefuj.append(row['por'])
    #     linkfuj.append(row['link'])
    #     nomefuj.append(row['nome'])

    # for i in 

    # for index,row in join_2_dfs.iterrows(): 
    #     priceml=json.dumps(row['price'])
    #     linkml=row['permalink']
    #     titleml=row['title']
    #     pricefuj=row['por']
    #     linkfuj=row['link']
    #     nomefuj=row['nome'] 
    #     print(nomefuj)

    #     c.execute('''
    #         INSERT INTO price(priceml,pricefuj)
    #         VALUES (?,?)
    #     ''',(priceml,pricefuj))
    #     c.execute('''
    #         INSERT INTO link(linkml,linkfuj)
    #         VALUES (?,?)
    #     ''',(linkml,linkfuj))
    #     c.execute('''
    #         INSERT INTO nome(nomeml,nomefuj)
    #         VALUES (?,?)
    #     ''',(titleml,nomefuj))

    db.commit()
    c.close()
    db.close()


def gerar_db():

    db=sqlite3.connect('bomdia.sqlite')
    c=db.cursor()

    q=c.execute('''
        SELECT * FROM fujioka
    ''')

    df=pd.read_sql('select * from fujioka',db)

    lista_de_nomes_fujioka = []

    for index, row in df.iterrows():
        lista_de_nomes_fujioka.append(row['nome'])

    lista_de_links_mercadolivre = []
    for i in lista_de_nomes_fujioka:
        lista_de_links_mercadolivre.append(
            f'https://lista.mercadolivre.com.br/{i}')

    print('Enviando Resquests Para Mercadolivre')

    resp = grequests.map([grequests.get(i)
                         for i in lista_de_links_mercadolivre])

    print('Salvando No DB')

    c.execute("DROP TABLE IF EXISTS produtos;")
    c.execute('''CREATE TABLE produtos(
            "id" TEXT,
            "official_store" TEXT,
            "bookmarked" BOOL,
            "discount_source" TEXT,
            "seller_info" TEXT,
            "permalink" TEXT,
            "pictures" TEXT,
            "price" TEXT,
            "title" TEXT,
            "subtitles" TEXT,
            "vertical" TEXT,
            "is_ad" BOOL,
            "installments" TEXT,
            "tags" TEXT,
            "image_ratio" REAL,
            "category_id" TEXT,
            "pictures_quantity" INTEGER,
            "rebates" TEXT,
            "vertical_highlight" TEXT,
            "value_propositions" TEXT,
            "available_quantity" INTEGER,
            "shipping" TEXT,
            "ad_label" TEXT,
            "ad_version" TEXT,
            "product" TEXT,
            "reviews" TEXT,
            "highlight" TEXT,
            "details" TEXT,
            "item_highlight" TEXT,
            "variations_picker" TEXT,
            "variations" TEXT
        )''')

    df_produtos = pd.DataFrame()
    temp_df=pd.DataFrame()

    for r in resp:

        soup = BeautifulSoup(r.content, features="html.parser")
        scripts_tags = soup.find_all('script')
        result = None

        for q in scripts_tags:
            search = re.search(
                "window.__PRELOADED_STATE__ =\n     (.+);", q.text)
            if search != None:
                result = search
                break
        try:
            if result.group(1) != None:
                print('Acho algo no RE')
                dump = json.loads(result.group(1))
                temp_df= pd.DataFrame(dump['initialState']['results'])
                
                # name = dump['initialState']['results'][0]['title']
                df_produtos = pd.concat([df_produtos, temp_df])
        except:
            print('Saiu do if por causa do NoneType')

    df_produtos.to_csv('tmp', index=False)
    aux = pd.read_csv('tmp')
    aux.to_sql('mercadolivre', db, if_exists='replace', index=False)


def consulta_db():

    # exemplo
    # select * from produto
    # left Join link on link.linkid =produto.linkid
    # left join price on price.priceid=produto.priceid
    # left join nome on nome.nomeid=produto.nomeid
    # where nomefuj||nomeml like '%teclado%'

    print('1- Consultar\n2- Criar db fujioka com ml\n3- Exit')
    query=input('Qual: ')

    match query:
        case '1':
            pd.set_option('max_rows', None)
            pd.set_option('max_columns', None)
            pd.set_option('colheader_justify', 'center')
            pd.set_option('precision', 3)
            stmt=input('Pesquisa: ')
            db=sqlite3.connect('bomdia.sqlite')
            c=db.cursor()

            query=pd.read_sql(f'''SELECT * FROM pesquisa WHERE pesquisa='{stmt}' ORDER BY RANK''',db)
            nomeml=pd.read_sql(f'''SELECT nomeml FROM pesquisa WHERE pesquisa='{stmt}' ORDER BY RANK''',db)
            nomefuj=pd.read_sql(f'''SELECT nomefuj FROM pesquisa WHERE pesquisa='{stmt}' ORDER BY RANK''',db)
            linkml=pd.read_sql(f'''SELECT linkml FROM pesquisa WHERE pesquisa='{stmt}' ORDER BY RANK''',db)
            linkfuj=pd.read_sql(f'''SELECT linkfuj FROM pesquisa WHERE pesquisa='{stmt}' ORDER BY RANK''',db)
            priceml=pd.read_sql(f'''SELECT priceml FROM pesquisa WHERE pesquisa='{stmt}' ORDER BY RANK''',db)
            pricefuj=pd.read_sql(f'''SELECT pricefuj FROM pesquisa WHERE pesquisa='{stmt}' ORDER BY RANK''',db)
            for index,row in query.iterrows():
                print('Nome do produto: ',row['nomefuj'],'\n','preco fuj: ',row['pricefuj'],'\n','lista de preco ml',row['priceml'],'\n','link fuj: ',row['linkfuj'],'\n','lista de link ml',row['linkml'],'\n')
            # preco_filtrado=query[query.priceml > query.pricefuj] 
            # print(preco_filtrado)
            c.close()
            db.close()
        case '2':
            criar_db_fujioka_com_ml(0,int(input('Passar ate q pag para salvar: ')))
        case '3':
            return

if __name__ == "__main__":
    # gerar_db(0, 2)
    consulta_db()
    # criar_db_fujioka_com_ml(0,30)
    # fujioka_gerar_html_page()

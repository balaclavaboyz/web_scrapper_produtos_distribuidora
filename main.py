import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
# from webdriver_manager.firefox import GeckoDriverManager

# primeira pagina deve ser pelo menos 1 ou maior
# ultima pagina, nao tem limite, mas na informatica aparentimente tem ate pagina 90, mas os produtos vao ate o numero 25-30
# nome em string


def scraper_loop_pags_fujioka_area_informatica_to_cvs(primeria_pagina, ultima_pagina, nome_do_csv):
    productList = []
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

    produtoLista = []
    for x in range(primeria_pagina, ultima_pagina):
        print(f'Pagina={x}')
        s = requests.Session()
        r = s.get(
            f'https://www.fujiokadistribuidor.com.br/buscapagina?fq=C%3a%2f11%2f&PS=32&sl=e26b41c8-257e-4456-9760-9217930ec898&cc=32&sm=0&PageNumber={x}', headers=headers)
        # print(s)
        # response = requests.request("GET", , )

        soup = BeautifulSoup(r.content, features="html.parser")

        productList = soup.find_all('span', class_='price')

        for bloco_de_span in productList:
            for item in bloco_de_span.find_all('a', href=True):
                endereco = item['href']
                # print(endereco)
                nome = item['title']
                # print(name)
                # print(item.text.split())
                # print(item.text.split()[2])

                de = item.text.split()[2]
                try:
                    por = item.text.split()[5]
                except:
                    por='0'
                try:
                    qnt_de_parcelas = item.text.split()[6]
                except:
                    qnt_de_parcelas = 'null'
                try:
                    cada_parcela = item.text.split()[9]
                except:
                    cada_parcela = 0

                produto = {
                    'nome': nome,
                    'de': de,
                    'por': por,
                    'qnt_de_parcelas': qnt_de_parcelas,
                    'cada_parcela': cada_parcela,
                    'link': endereco
                }
                # print(produto)
                print('Salvando: ', produto['nome'])
                produtoLista.append(produto)

    df = pd.DataFrame(produtoLista)

    return df.to_csv(nome_do_csv, index=False, encoding='utf-8')


def mercadolivre_search_product_first_page_selenium(nome):


    product = input('Nome do produto: ')
    # product='ddr4'
    s = Service(GeckoDriverManager().install())

    options = webdriver.FirefoxOptions()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    options.headless = True

    driver = webdriver.Firefox(options=options, service=s)

    driver.get('https://www.mercadolivre.com.br/')
    # driver.maximize_window()
    sleep(2)
    search = driver.find_element_by_xpath('/html/body/header/div/form/input')
    # search = driver.find_element(By.XPATH('/html/body/header/div/form/input'))
    search.send_keys(product)
    search.send_keys(Keys.ENTER)
    sleep(3)
    # se voce quiser fazer por menor preco
    # dropdown=driver.find_element_by_xpath('/html/body/main/div/div[1]/section/div[1]/div/div/div/div[2]/div/div/button')
    # dropdown.click()
    # menor_preco=driver.find_element_by_xpath('/html/body/main/div/div[1]/section/div[1]/div/div/div/div[2]/div/div/div/ul/a[1]')
    # menor_preco.click()
    # sleep(3)

    titulos = driver.find_elements_by_css_selector(
        "h2.ui-search-item__group__element.ui-search-item__title")
    listaTitulos = []
    for i in titulos:
        listaTitulos.append(i.text)

    precos_inteiro = driver.find_elements_by_css_selector(
        "div.ui-search-price.ui-search-price--size-medium.ui-search-item__group__element > div.ui-search-price__second-line > span.price-tag.ui-search-price__part > span.price-tag-amount > span.price-tag-fraction")
    listaPrecosInteiro = []
    for j in precos_inteiro:
        listaPrecosInteiro.append(j.text)

    links = driver.find_elements_by_css_selector(
        "div.andes-card.andes-card--flat.andes-card--default.ui-search-result.ui-search-result--core.andes-card--padding-default.andes-card--animated > div.ui-search-result__image > a.ui-search-link")
    listaLinks = []
    for m in links:
        listaLinks.append(m.get_attribute('href'))

    data = []
    data.append(listaTitulos)
    data.append(listaPrecosInteiro)
    data.append(listaLinks)

    df = pd.DataFrame(data).transpose()
    df.columns = ['Nome', 'Preco', 'Link']

    driver.close()

    return df.to_csv(nome, encoding='utf-8')

def db():
    conn = sqlite3.connect('bomdia.db')
    c = conn.cursor()
    df = pd.read_csv('df.csv')
    df.to_sql('produto', conn, if_exists='append', index=False)

def mercadolivre_requests():

    product = input('Nome do produto: ')

    s = requests.Session()
    r = s.get(f'https://lista.mercadolivre.com.br/{product}')

    soup = BeautifulSoup(r.content, features="html.parser")
    scripts_tags = soup.find_all('script')
    result = None

    for q in scripts_tags:
        search = re.search("window.__PRELOADED_STATE__ =\n     (.+);", q.text)
        if search != None:
            result = search
            break

    var = json.loads(result.group(1))

    with open('json.json', 'w') as f:
        json.dump(var, f, indent=4)

    df_produtos = pd.DataFrame(var['initialState']['results'])
    df_produtos.to_csv('df.csv', index=False)

def mercadolivre_requests_plus_db(product):
    print('criando session do mercadolivre')

    r = requests.Session().get(f'https://lista.mercadolivre.com.br/{product}')

    soup = BeautifulSoup(r.content, features="html.parser")
    scripts_tags = soup.find_all('script')
    result = None

    print(f'pesquisando o produto: {product}')
    for q in scripts_tags:
        search = re.search("window.__PRELOADED_STATE__ =\n     (.+);", q.text)
        if search != None:
            result = search
            break

    if result.group(1)==None:
        return
    var = json.loads(result.group(1))


    df_produtos = pd.DataFrame(var['initialState']['results'])
    df_produtos.to_csv('temp', index=False)

    conn = sqlite3.connect('bomdia.db')
    c = conn.cursor()
    df = pd.read_csv('temp')
    df.to_sql(product, conn,if_exists='replace', index=False)
    c.close()

    print(f'salvo no db como um tab com nome: {product}')

def auto_fujioka_mercadolivre_db(primeria_pagina,ultima_pagina):
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

    produtoLista = []
    for x in range(primeria_pagina, ultima_pagina):
        print(f'Pagina={x}')
        r = requests\
            .Session()\
            .get(f'https://www.fujiokadistribuidor.com.br/buscapagina?fq=C%3a%2f11%2f&PS=32&sl=e26b41c8-257e-4456-9760-9217930ec898&cc=32&sm=0&PageNumber={x}', headers=headers)

        soup = BeautifulSoup(r.content, features="html.parser")

        productList = soup.find_all('span', class_='price')

        for bloco_de_span in productList:
            for item in bloco_de_span.find_all('a', href=True):
                endereco = item['href']
                nome = item['title']

                de = item.text.split()[2]
                try:
                    por = item.text.split()[5]
                except:
                    por='0'
                try:
                    qnt_de_parcelas = item.text.split()[6]
                except:
                    qnt_de_parcelas = 'null'
                try:
                    cada_parcela = item.text.split()[9]
                except:
                    cada_parcela = 0

                produto = {
                    'nome': nome,
                    'de': de,
                    'por': por,
                    'qnt_de_parcelas': qnt_de_parcelas,
                    'cada_parcela': cada_parcela,
                    'link': endereco
                }
                # print(produto)
                print('Salvando: ', produto['nome'])
                produtoLista.append(produto)

    df = pd.DataFrame(produtoLista)
    # print(df)
    
    for index,row in df.iterrows():
        mercadolivre_requests_plus_db(row['nome'])

    # return df.to_csv(nome_do_csv, index=False, encoding='utf-8')
if __name__ == "__main__":

    scraper_loop_pags_fujioka_area_informatica_to_cvs(1,35,'bomdia')
    # mercadolivre_search_product_first_page_selenium('mercadolivre_pesquisa.csv')
    # mercadolivre_requests()
    # db()

    # mercadolivre_requests_plus_db()

    # auto_fujioka_mercadolivre_db(0,10)

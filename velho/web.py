import requests
# from bs4 import BeautifulSoup
import json

# s = requests.Session()
# jar=requests.cookies.RequestsCookieJar()
# jar.set('sback_access_token','eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuc2JhY2sudGVjaCIsImlhdCI6MTYzNTYzNDkzMiwiZXhwIjoxNjM1NzIxMzMyLCJhcGkiOiJ2MiIsImRhdGEiOnsiY2xpZW50X2lkIjoiNjBmNzA2YjdkM2E1ZjZhMjkzN2RhMjM0IiwiY2xpZW50X2RvbWFpbiI6ImZ1amlva2FkaXN0cmlidWlkb3IuY29tLmJyIiwiY3VzdG9tZXJfaWQiOiI2MTdkY2VmNDQ5OWNjNjUzNmIxOWEwZjYiLCJjdXN0b21lcl9hbm9ueW1vdXMiOnRydWUsImNvbm5lY3Rpb25faWQiOiI2MTdkY2VmNDQ5OWNjNjUzNmIxOWEwZjciLCJhY2Nlc3NfbGV2ZWwiOiJjdXN0b21lciJ9fQ.FJrFjZBEyDSbp4lX7jLUw8MyKN-kLHWpVhserZsXDtI.WrWruyKqDruyKqzRHeKqgP')
# s.cookies=jar
# r= s.get('https://www.fujiokadistribuidor.com.br/informatica')
# print(r.content)



# ---

# urlLogin='https://www.fujiokadistribuidor.com.br/api/vtexid/pub/authentication/start'
# # eh json a res

# email='milvestcontato+03897792000137@gmail.com'

# def login(email):
#     s=requests.Session()
#     payload={
#         'user':email
#     }
#     res=s.post(urlLogin,json=payload)
#     print(res.content)

# login(email)

# ---

# baseurl = 'https://www.fujiokadistribuidor.com.br/'

# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
# }

# r=requests.get('https://www.fujiokadistribuidor.com.br/informatica')

# soup=BeautifulSoup(r.content,'html')

# productlist=soup.find_all('span',class_='price')

# print(productlist)

import requests

url = "https://www.fujiokadistribuidor.com.br/informatica"

payload={}
headers = {
  'authority': 'www.fujiokadistribuidor.com.br',
  'pragma': 'no-cache',
  'cache-control': 'no-cache',
  'sec-ch-ua': '"Microsoft Edge";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.38',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-user': '?1',
  'sec-fetch-dest': 'document',
  'referer': 'https://www.fujiokadistribuidor.com.br/',
  'accept-language': 'en-US,en;q=0.9',
  'cookie': 'ISSMB=ScreenMedia=0&UserAcceptMobile=False; janus_sid=546154e5-a989-4a95-bd4f-953e4c8c351a; VtexRCMacIdv7=fe1c8abc-37c0-4c86-b8c7-f687ea6f6a28; _gcl_au=1.1.1449848979.1635634922; checkout.vtex.com=__ofid=6a00a161e35b4016a5ce6f5c6360ab88; _gid=GA1.3.1179165909.1635634922; _fbp=fb.2.1635634922241.709457195; nav_id=0421c45a-d28c-4c57-8b7e-1dc75e59df42; .ASPXAUTH=B676348D663E604972EBFED081D6F456E37D184F03B67280FD3ADC8A6AD180D77F515824D4CB43CD8D2E394906145ADE8F03CE28917A8B00F25FFDB9C155CCA63D8624A114175A919D0C644C797116B2BF0DC629BFC735B6E2EB54CBF40C4B2D7EB2755263D62ECE8459F13DD9206A77CFCF432845B1D674B4855036B554BFFF2DCCE40DF7F3D5DB70D5F4AEECD6E576783C32C06C169EE896FD55DE3DC2379097AEC93B; blueID=7cdef02f-a532-446a-84d2-170b6f728666; _hjFirstSeen=1; _hjid=4c335acc-ca14-4936-954c-ccc3a355cbd6; _hjAbsoluteSessionInProgress=0; legacy_p=0421c45a-d28c-4c57-8b7e-1dc75e59df42; chaordic_browserId=0421c45a-d28c-4c57-8b7e-1dc75e59df42; legacy_c=0421c45a-d28c-4c57-8b7e-1dc75e59df42; legacy_s=0421c45a-d28c-4c57-8b7e-1dc75e59df42; __bid=7721e8c0-a2d7-4846-acdf-89cf7ba77e27; tt.u=0100007FF2CE7D614106AE2F029D8C24; tt.nprf=; voxusmediamanager_id=16356349249720.9691854151952648snt0hcs5vqk; sback_browser=0-52594900-163563493199ed6ab855de6cfa8d3c8fea10d0922a23308313635385417617dcef38068b9-96310250-179931719,524643163-1635634931; voxusmediamanager_acs=true; sback_client=60f706b7d3a5f6a2937da234; sback_customer=$2QaysURypHUOB1aq50dXFkWn1GbSdDRC5Ub1Y2a2p3SZRla1oVUU5kTspXVZdla1kFe4Z1aaRFZZh0dQl1VtdkT2$12; sback_access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuc2JhY2sudGVjaCIsImlhdCI6MTYzNTYzNDkzMiwiZXhwIjoxNjM1NzIxMzMyLCJhcGkiOiJ2MiIsImRhdGEiOnsiY2xpZW50X2lkIjoiNjBmNzA2YjdkM2E1ZjZhMjkzN2RhMjM0IiwiY2xpZW50X2RvbWFpbiI6ImZ1amlva2FkaXN0cmlidWlkb3IuY29tLmJyIiwiY3VzdG9tZXJfaWQiOiI2MTdkY2VmNDQ5OWNjNjUzNmIxOWEwZjYiLCJjdXN0b21lcl9hbm9ueW1vdXMiOnRydWUsImNvbm5lY3Rpb25faWQiOiI2MTdkY2VmNDQ5OWNjNjUzNmIxOWEwZjciLCJhY2Nlc3NfbGV2ZWwiOiJjdXN0b21lciJ9fQ.FJrFjZBEyDSbp4lX7jLUw8MyKN-kLHWpVhserZsXDtI.WrWruyKqDruyKqzRHeKqgP; sback_partner=false; sb_days=1635634926735; sback_customer_w=true; i18next=pt-BR; sback_refresh_wp=no; SGTP=UGUIDReturn=True; VTEXSC=sc=1; VtexIdclientAutCookie_fujiokadistribuidor=eyJhbGciOiJFUzI1NiIsImtpZCI6IjM5NUU5OTA1QjFGOTk2RjEwNzcxMTI0ODZBMTE3QzA0RDY3NjMzOUMiLCJ0eXAiOiJqd3QifQ.eyJzdWIiOiJtaWx2ZXN0Y29udGF0byswMzg5Nzc5MjAwMDEzN0BnbWFpbC5jb20iLCJhY2NvdW50IjoiZnVqaW9rYWRpc3RyaWJ1aWRvciIsImF1ZGllbmNlIjoid2Vic3RvcmUiLCJzZXNzIjoiNmVmNmE2MTYtNzI0Mi00ZDQ2LWE5MWEtNDFiYjk0Yzk2MGRkIiwiZXhwIjoxNjM1NzIzMTI0LCJ1c2VySWQiOiIyYzAzMjhjZC02ZjBiLTQwNjYtOGY4Ni04YjZmZDg4MzVlMDciLCJpYXQiOjE2MzU2MzY3MjQsImlzcyI6InRva2VuLWVtaXR0ZXIiLCJqdGkiOiJhZWUzMjJiYi04YzdhLTQxYmItYTJmZC0zZTAyYjAyZDVlZDEifQ.0xATCm765RBDtFRKENfJ2_YJ-5dI6BtvVn6QlewimJ-IOFtmxqCIkBVsNEI2Hw_XVSEGhi8pUBPXceuiYvmCQw; VtexIdclientAutCookie_4a52d56b-bab5-406e-b928-959a7988a95f=eyJhbGciOiJFUzI1NiIsImtpZCI6IjM5NUU5OTA1QjFGOTk2RjEwNzcxMTI0ODZBMTE3QzA0RDY3NjMzOUMiLCJ0eXAiOiJqd3QifQ.eyJzdWIiOiJtaWx2ZXN0Y29udGF0byswMzg5Nzc5MjAwMDEzN0BnbWFpbC5jb20iLCJhY2NvdW50IjoiZnVqaW9rYWRpc3RyaWJ1aWRvciIsImF1ZGllbmNlIjoid2Vic3RvcmUiLCJzZXNzIjoiNmVmNmE2MTYtNzI0Mi00ZDQ2LWE5MWEtNDFiYjk0Yzk2MGRkIiwiZXhwIjoxNjM1NzIzMTI0LCJ1c2VySWQiOiIyYzAzMjhjZC02ZjBiLTQwNjYtOGY4Ni04YjZmZDg4MzVlMDciLCJpYXQiOjE2MzU2MzY3MjQsImlzcyI6InRva2VuLWVtaXR0ZXIiLCJqdGkiOiJhZWUzMjJiYi04YzdhLTQxYmItYTJmZC0zZTAyYjAyZDVlZDEifQ.0xATCm765RBDtFRKENfJ2_YJ-5dI6BtvVn6QlewimJ-IOFtmxqCIkBVsNEI2Hw_XVSEGhi8pUBPXceuiYvmCQw; vtex_session=eyJhbGciOiJFUzI1NiIsImtpZCI6IkMwMDUzNDVBMkM5MTFGRUFFMzQzOUNBNUMxNDZCNTYwNjdEODQxM0UiLCJ0eXAiOiJqd3QifQ.eyJhY2NvdW50LmlkIjoiNGE1MmQ1NmItYmFiNS00MDZlLWI5MjgtOTU5YTc5ODhhOTVmIiwiaWQiOiI0OTBiOTNhOC02YTlhLTQxZWYtYWViNy03MzM3MmUxNjM2YTIiLCJ2ZXJzaW9uIjo2LCJzdWIiOiJzZXNzaW9uIiwiYWNjb3VudCI6InNlc3Npb24iLCJleHAiOjE2MzYzMjc5MjUsImlhdCI6MTYzNTYzNjcyNSwiaXNzIjoidG9rZW4tZW1pdHRlciIsImp0aSI6ImM2ZDU0ZGUwLWI5MmQtNDI4My05YzRhLTgzOGFjYzUwOTY3OCJ9.eZtF7gN8ITF19zUp8bUZ6FRJIzFZYCL_jC4h_UvWtzWABTn_W8bLXN01TDgAoFXx0CJFXOj2eGgN6xJcEn2sKA; vtex_segment=eyJjYW1wYWlnbnMiOm51bGwsImNoYW5uZWwiOiIxIiwicHJpY2VUYWJsZXMiOiJVRkRTUC1MVDMzLUNUMDEtU1UwMC1ERTAwLVNJMDAtQ1MwMSIsInJlZ2lvbklkIjpudWxsLCJ1dG1fY2FtcGFpZ24iOm51bGwsInV0bV9zb3VyY2UiOm51bGwsInV0bWlfY2FtcGFpZ24iOm51bGwsImN1cnJlbmN5Q29kZSI6IkJSTCIsImN1cnJlbmN5U3ltYm9sIjoiUiQiLCJjb3VudHJ5Q29kZSI6IkJSQSIsImN1bHR1cmVJbmZvIjoicHQtQlIiLCJhZG1pbl9jdWx0dXJlSW5mbyI6InB0LUJSIiwiY2hhbm5lbFByaXZhY3kiOiJwdWJsaWMifQ; IPI=UsuarioGUID=2c0328cd-6f0b-4066-8f86-8b6fd8835e07; SGTS=6C83EE5EC362FF6BE9DBABEDF0B9570C; urlLastSearch=http://www.fujiokadistribuidor.com.br/informatica; VtexRCSessionIdv7=ecd9b2ac-6cee-4c74-aec6-d87078b0dc9a; impulsesuite_session=1635638967167-0.9453070368557885; _st_ses=33106969627469685; _st_id=bmV3LmV5SjBlWEFpT2lKS1YxUWlMQ0poYkdjaU9pSklVekkxTmlKOS5leUpsYldGcGJDSTZJbTFwYkhabGMzUmpiMjUwWVhSdlFHZHRZV2xzTG1OdmJTSjkuT1d4Mnp3WG1SU0M3cUUyczUzTmYtY2FqX3BNQWx4cjRnTTlSMXJtUmNxYy5XcldydXlLcURydXlLcWlZSGVFaUtx; _st_cart_url=/; _st_cart_script=helper_impulse_meta.js; tt_c_vmt=1635638968; tt_c_s=direct; tt_c_m=direct; tt_c_c=direct; _st_no_user=1; sback_total_sessions=2; sback_current_session=1; voxusmediamanager__ip=179.93.171.9; _ga_KRSKYCLYL9=GS1.1.1635638966.2.1.1635638988.0; _ga=GA1.1.1001357842.1635634922; _spl_pv=13; _ttuu.s=1635638989949'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.content)

import re

from bs4 import BeautifulSoup
import requests
import time
import datetime
import mysql.connector
#ICO: ~ PHM of 3,000,000,000|ICO: 500,000 PUFFS ~|ICO: ~ MDC ~|ICO: 510,000,000 DOR of 1,000,000,000
amount = ''
total = ''
aaa ="ICO: 510,000,000 DOR of 1,000,000,000"
aaa=re.sub('[,]', '', aaa)
ss = re.sub('[\d]', '', aaa)
token = re.split(r"[\s]", aaa)[2]
if (aaa == ss):
    amount = ''
    total = ''
else:
    am = re.split(r"[\s]", aaa)[1]
    if(am=='~'):
        amount=''
        total=re.split(r"[\s]", aaa)[4]
    else:
        amount = re.split(r"[\s]", aaa)[1]
        if(re.split(r"[\s]", aaa)[3]=='~'):
            total = ''
        else:

            total = re.split(r"[\s]", aaa)[4]
print(total)
print('dddddddd')
print(amount)
# bb = re.sub('[\d]', '', aaa)

# aa = re.sub('[:a-zA-Z]', '', aaa)
# token = re.split(r"[\s]", bb)[2]
# amount = re.split(r"[\s]", aa)[1]
# total = re.sub(r"[~]", aa)
# if (re.split(r"[\s]", aa)[4]):
#     total = re.split(r"[\s]", aa)[4]
# else:
#     total = ''

# print(total)

#print(amount)
# #token = re.split(r"[\s]", bb)
# #aa = re.sub('[:a-zA-Z]', '', aaa)
#
# amount = re.sub(r"[\s]",r'-', aaa)
#
# #total = re.split(r"[\s]", aa)
# print (amount)

# source_link='https://www.facebook.com/pg/eosblockchain/posts/?ref=page_internal'
# response1 = requests.get(source_link)
# html1 = response1.content
# location=''
# content1 = BeautifulSoup(html1,'html.parser')
# content=''
# share='0'
# if (content1.findAll('div', attrs={'class': '_5pcr userContentWrapper'})):
#     for body in content1.findAll('div', attrs={'class': '_5pcr userContentWrapper'}):
#         name=body.find('span',attrs={'class':'fwn fcg'}).find('a').get_text()
#         time=body.find('div',attrs={'class':'_5pcp _5lel'}).find('span',attrs={'class':'fsm fwn fcg'}).find('abbr')['title']
#         if(body.find('div',attrs={'class':'_5pbx userContent'})):
#          content=body.find('div',attrs={'class':'_5pbx userContent'}).get_text()
#         if(body.find('div',attrs={'class':'uiUfi UFIContainer _5pc9 _5vsj _5v9k'}).find('div',attrs={'class':'UFIList'})):
#             # share=body.find('div',attrs={'class':'UFIRow UFIShareRow'}).find('a').get_text()
#             # share=re.sub('[:a-zA-Z]', '', share)
#             share=8
#         print(share)
#
#
# # img = content1.find('div', attrs={'class': '_5va1 _427x'}).findAll('img')
# # print(body)
# # print(img)
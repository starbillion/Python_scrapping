from bs4 import BeautifulSoup
import requests
import mysql.connector
conn = mysql.connector.connect(host='localhost',database='src',user='root',password='')
x = conn.cursor()
def token_price(url,token):
    response = requests.get(url)
    html = response.content
    content = BeautifulSoup(html, 'html.parser')
    open=''
    date=''
    high=''
    low=''
    close=''
    volume=''
    cap=''
    if(content.find('div',attrs={'id':'historical-data'}).find('tbody').findAll('tr',attrs={'class':'text-right'})):
        id=0
        for row in content.find('div',attrs={'id':'historical-data'}).find('tbody').findAll('tr'):
            id=id+1
            date= row.findAll('td')[0].get_text()
            open = row.findAll('td')[1].get_text()
            high = row.findAll('td')[2].get_text()
            low = row.findAll('td')[3].get_text()
            close = row.findAll('td')[4].get_text()
            volume = row.findAll('td')[5].get_text()
            cap = row.findAll('td')[6].get_text()
            x.execute(
                "INSERT INTO token_prices(id,token,dates,opens,high,low,clos,volume,cap) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (id,token,date,open,high,low,close,volume,cap))
            conn.commit()


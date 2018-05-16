import re

from bs4 import BeautifulSoup
import requests
import time
import datetime
import mysql.connector
import tokens
conn = mysql.connector.connect(host='localhost',database='src',user='root',password='')

ico_url_array = ['https://icotracker.net/current',
                 'https://icotracker.net/upcoming',
                 'https://icotracker.net/past']


def start_scrapping(conn):
    x = conn.cursor()
    x.execute("TRUNCATE TABLE ico_links")
    x.execute("TRUNCATE TABLE icos")
    x.execute("TRUNCATE TABLE token_links")
    x.execute("TRUNCATE TABLE token_prices")
    x.execute("TRUNCATE TABLE tokens")
    x.execute("TRUNCATE TABLE twitter")
    x.execute("TRUNCATE TABLE facebook")
    ico_id=0
    for ico_url in ico_url_array:
        response = requests.get(ico_url)
        html = response.content

        content = BeautifulSoup(html,'html.parser')
        table = content.find('div', attrs={'class': 'container-wrp container-fluid block-indent'}).findAll('div',attrs={'class': 'row'})[1]
        cnt = 0
        # for ta in table:
        for row in table.find_all('div', attrs={'class': 'col-12 col-lg-6 col-xl-4'}):
            ico_id=ico_id+1
            ico_name = row.find('div', attrs={'class': 'flex-first cp-col-sm col-9 col-sm-9 cp-prj'}).find('h2').get_text()

            #insert token table
            token_name = re.sub(r"[\s]", r'-', ico_name)
            tokens.get_token(token_name)
            #end

            # insert ico_link
            social = row.find('div', attrs={'class': 'cp-social'})
            for social_a in social.findAll('a'):
                ico_link = social_a['href']
                social_name =social_a['title']
                ico_links(conn,ico_id,ico_link,social_name)
            # end ico_link

            if(row.find('div', attrs={'class': 'cp-col col-9 col-sm-9 cp-info'}).find('div',attrs={'class': 'alert alert-danger'})):
                scam = "True"
            else:
                scam = "False"
            ico_desc = row.find('div', attrs={'class': 'cp-row-sm row cp-prj-descr'}).find('div', attrs={'class': 'cp-col-sm col-12'}).get_text()

            footer_part = row.find('div', attrs={'class': 'cp-row row cp-body'}).find('div', attrs={'class': 'cp-col col-9 col-sm-9 cp-info'})

            # left part of bottome of title
            footer_part_left = footer_part.find('div',attrs={'class':'cp-info-i'}).find('div',attrs={'class':'cp-col-sm col-12 col-sm cp-what'}).findAll('div',attrs={'class':'cp-line'})

            base = footer_part_left[0].find('span',attrs={'class','text-black'}).get_text()
            if(footer_part_left[1].find('a', attrs={'target': '_blank','href': True})):
                 whitepaper_url = footer_part_left[1].find('a', attrs={'target': '_blank','href': True})['href']
            if(footer_part_left[2].find('i',attrs={'class','fa fa-close'})):
                escrow = "False"
            elif (footer_part_left[2].find('i',attrs={'class','fa fa-check text-warning'})):
                escrow = "True"

            footer_part_right = footer_part.find('div',attrs={'class':'cp-info-i'}).find('div',attrs={'class':'cp-col-sm col-12 col-sm cp-who'}).findAll('div',attrs={'class':'cp-line'})

            # getting homepage url
            homepage = footer_part_right[1].find('a', attrs={'target': '_blank', 'href': True})['href']
            # getting ceo_name
            if(footer_part_right[2].find('span')):

                ceo_name = footer_part_right[2].find('span').get_text()
            else:
                ceo_name = ''
            # geeting ceo_link
            if(footer_part_right[2].find('a')):

                ceo_link = footer_part_right[2].find('a', attrs={'target': '_blank', 'href': True})['href']
            else:
                ceo_link = ''

            if (scam == "False"):
                # getting ico_link
                if(footer_part.find('div',attrs={'class':'cp-ico-o'}).find('a',attrs={'target':'_blank', 'href': True})):
                    ico_link = footer_part.find('div',attrs={'class':'cp-ico-o'}).find('a',attrs={'target':'_blank', 'href': True})['href']
                else:
                    ico_link = ''
                #     getting amount and total
                aaa = footer_part.find('div', attrs={'class': 'cp-ico-o'}).find('span',attrs={'class':'text-black'}).get_text()
                aaa = re.sub('[,]', '', aaa)
                ss = re.sub('[\d]', '', aaa)
                token = re.split(r"[\s]", aaa)[2]
                if (aaa == ss):
                    amount = ''
                    total = ''
                else:
                    am = re.split(r"[\s]", aaa)[1]
                    if (am == '~'):
                        amount = ''
                        total = re.split(r"[\s]", aaa)[4]
                    else:
                        amount = re.split(r"[\s]", aaa)[1]
                        if (re.split(r"[\s]", aaa)[3] == '~'):
                            total = ''
                        else:
                            total = re.split(r"[\s]", aaa)[4]


            #     getting lauch, end, bonus, bitcoin
                if (footer_part.findAll('div', attrs={'class': 'cp-row-sm row'})):
                    temp = footer_part.findAll('div', attrs={'class': 'cp-row-sm row'})
                    launch_end = temp[1].find('span',attrs={'class':'text-black'}).get_text()

                    if(bool(re.search(r'\d', launch_end))):
                        launch = re.split(" UTC - ", launch_end)[0]
                        ico_end = re.split(" UTC - ", launch_end)[1]
                    else:
                        launch = ''
                        ico_end = ''

                    bonus = temp[2].find('div',attrs={'class':'cp-line'}).findAll('span', attrs={'class': 'text-black'})[0].get_text()

                    # removing <text>B</text>
                    temp[2].find('div',attrs={'class':'cp-line'}).findAll('span', attrs={'class': 'text-black'})[1].find('text').decompose()

                    bitcoin = temp[2].find('div', attrs={'class': 'cp-line'}).findAll('span', attrs={'class': 'text-black'})[1].get_text()

                else:
                    launch = ''
                    ico_end = ''
                    bonus = ''
                    bitcoin = ''

                if (row.find('div', attrs={'class': 'cp-row row cp-body'}).find('div', attrs={'class': 'cp-chart-digs font-alt'})):
                    cp = row.find('div', attrs={'class': 'cp-row row cp-body'}).find('div', attrs={'class': 'cp-chart-digs font-alt'}).find('strong').get_text()
                    if(bool(re.search(r'\d', cp)) == False):
                        cp = ''
                else:
                    cp = ''

            else:
                ico_link = ''
                amount = ''
                total = ''

            # Insert new employee
            x.execute("INSERT INTO icos(id,ico_name,scam,ico_desc,base,whitepaper_url,escrow,homepage,ceo_name,ceo_link,ico_link,amount,total,launch,ico_end,bonus,bitcoin,cp,token) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(ico_id,ico_name,scam,ico_desc,base,whitepaper_url,escrow,homepage,ceo_name,ceo_link,ico_link,amount,total,launch,ico_end,bonus,bitcoin,cp,token))
            conn.commit()
            cnt = cnt + 1
            print ("-------------------- ")
            if cnt >= 20:

                # db.close()
                break
    x.close()
# initial_db()
def ico_links(conn,ico_id,ico_link,social_name):
    x = conn.cursor()
    x.execute("insert into ico_links(ico_id,social_media,url) values (%s,%s,%s)",(ico_id,social_name,ico_link))
    conn.commit()



start_scrapping(conn)

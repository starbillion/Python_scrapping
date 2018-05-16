import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
import token_price
import tentative
import mysql.connector
conn = mysql.connector.connect(host='localhost',database='src',user='root',password='')
x = conn.cursor()
def get_token(token_url):
    token='https://coinmarketcap.com/currencies/'+token_url
    response = requests.get(token)
    html = response.content
    content = BeautifulSoup(html,'html.parser')
    #get platform
    if(content.find('h1', attrs={'class': 'text-large'})):
        plat = content.find('h1', attrs={'class': 'text-large'})
        platform=plat.find('img')['alt']

        #get token
        token1=content.find('small', attrs={'class': 'bold hidden-sm hidden-md hidden-lg'})
        token3=token1.get_text()
        token2 = re.sub(r"\(",r'', token3)
        token_name = re.sub(r"\)",r'', token2)
        #get token price table
        token_price_link=token+'/historical-data'
        token_price.token_price(token_price_link,token_name)
        #end
        #get announsment
        if(content.find('span', attrs={'title': 'Announcement'})):
            anno=content.find('span', attrs={'title': 'Announcement'}).find_next_sibling('a')['href']
        else:
            anno=''

        #get rank
        if(content.find('span', attrs={'class': 'label label-success'})):
            rank1=content.find('span', attrs={'class': 'label label-success'}).get_text()
            rank=re.sub('[:a-zA-Z\s+]', '', rank1)
        else:
            rank=''
        temp=content.find('div', attrs={'class': 'col-sm-8 col-sm-push-4'})
        #get token tags
        token_tags=''
        if(content.find('span',attrs={'title':'Tags'})):
            for tag in content.find('span',attrs={'title':'Tags'}).parent.findAll('small'):
                token_tags=token_tags+tag.get_text()+','

        #get cap
        cap_usd = ''
        cap_btc = ''
        cap_eth = ''
        for check in temp.findAll('h3', attrs={'class': 'details-text-medium'}):
            if check.get_text() == 'Market Cap':
                cap= check.parent.find_next_sibling()
                num=cap.findAll('span')[1].get_text()
                unit = cap.findAll('span')[2].get_text()
                if(unit=='USD'):
                    cap_usd =num
                if (unit == 'BTC'):
                    cap_btc = num
                if (unit == 'ETH'):
                    cap_eth = num
                cap1=check.parent.find_next_sibling().findAll('span',attrs={'class':'text-gray'})
                for aa in cap1:
                    bb=aa.get_text()
                    num1=re.sub('[:a-zA-Z\s+]', '', bb)
                    unit1=re.sub('[\d\s+,]', '', bb)
                    if (unit1 == 'USD'):
                        cap_usd = num1
                    if (unit1 == 'BTC'):
                        cap_btc = num1
                    if (unit1 == 'ETH'):
                        cap_eth = num1
        #get volume
        volume_usd = ''
        volume_btc = ''
        volume_eth = ''
        for check in temp.findAll('h3', attrs={'class': 'details-text-medium'}):
            if check.get_text() == 'Volume (24h)':
                cap= check.parent.find_next_sibling()
                num=cap.findAll('span')[1].get_text()
                unit = cap.findAll('span')[2].get_text()
                if(unit=='USD'):
                    volume_usd =num
                if (unit == 'BTC'):
                    volume_btc = num
                if (unit == 'ETH'):
                    volume_eth = num
                cap1=check.parent.find_next_sibling().findAll('span',attrs={'class':'text-gray'})
                for aa in cap1:
                    bb=aa.get_text()
                    num1=re.sub('[:a-zA-Z\s+]', '', bb)
                    unit1=re.sub('[\d\s+,]', '', bb)
                    if (unit1 == 'USD'):
                        volume_usd = num1
                    if (unit1 == 'BTC'):
                        volume_btc = num1
                    if (unit1 == 'ETH'):
                        volume_eth = num1
        #get Circulating
        circulating_supply = ''
        max_supply = ''
        for check in temp.findAll('h3', attrs={'class': 'details-text-medium'}):
            if check.get_text() == 'Circulating Supply':
                circulating_supply = check.parent.find_next_sibling().get_text()
                circulating_supply = re.sub('[\s+]','', circulating_supply)
        #get max

        # for check in temp.findAll('h3', attrs={'class': 'details-text-medium'}):
            if check.get_text() == 'Max Supply':
                max_supply = check.parent.find_next_sibling().get_text()
                max_supply = re.sub('[\s+]','', max_supply)
        #get total
        total_supply = ''
        for check in temp.findAll('h3', attrs={'class': 'details-text-medium'}):
            if check.get_text() == 'Total Supply':
                total_supply = check.parent.find_next_sibling().get_text()
                total_supply = re.sub('[\s+]', '', total_supply)
        #get git
        git_name=''
        git_des=''
        location=''
        git_repos=''
        git_people=''
        git_languages=''
        git_topic=''
        if(content.find('span',attrs={'title':'Source Code'})):
            source_link=content.find('span',attrs={'title':'Source Code'}).parent.find('a')['href']
            response1 = requests.get(source_link)
            html1 = response1.content
            content1 = BeautifulSoup(html1,'html.parser')
        #getgit name
            if(content1.find('h1',attrs={'class':'org-name lh-condensed'})):
               git_name=content1.find('h1',attrs={'class':'org-name lh-condensed'}).get_text()
               git_name=re.sub('[\s+]', '', git_name)
        #get git des
               if(content1.find('div', attrs={'class': 'TableObject-item TableObject-item--primary'}).find('div')):
                    git_des = content1.find('div', attrs={'class': 'TableObject-item TableObject-item--primary'}).find('div').get_text()
                    git_des = re.sub('[\s+]', '', git_des)
        #get git repos and people
               git_repos=content1.findAll('span', attrs={'class': 'Counter'})[0].get_text()
               git_people = content1.findAll('span', attrs={'class': 'Counter'})[1].get_text()
        #get git location
               if(content1.find('ul',attrs={'class':'org-header-meta has-location has-blog'})):
                   if(content1.find('ul',attrs={'class':'org-header-meta has-location has-blog'}).find('span',attrs={'itemprop':'location'})):
                       location=content1.find('ul',attrs={'class':'org-header-meta has-location has-blog'}).find('span',attrs={'itemprop':'location'}).get_text()

        #get git languages
               if(content1.findAll('include-fragment')):
                   for sr in content1.findAll('include-fragment'):
                        src=sr['src']
                        url="http://github.com"+src
                        response2 = requests.get(url)
                        html2 = response2.content
                        content2 = BeautifulSoup(html2, 'html.parser')
                        if(content2.find('h4')):
                            top=content2.find('h4').get_text()
                            if(top=='Most used topics'):
                                topic=content2.find('div',attrs={'class':'Box-body'}).findAll('a')
                                for top in topic:
                                    top=top.get_text()
                                    top=re.sub('[\s+]', '', top)
                                    git_topic=git_topic+top+','
                            if (top == 'Top languages'):
                                language = content2.find('div', attrs={'class': 'Box-body'}).findAll('a')
                                for lan in language:
                                    lan = lan.findAll('span')[1].get_text()
                                    git_languages = git_languages + lan + ','

        #get data from etherscan.io
        token_holders=''
        txn_no=''
        eth_address=''
        decimal=''
        reputation=''
        etherscan_link=''
        etherscan='https://etherscan.io/tokens'
        response3 = requests.get(etherscan)
        html3 = response3.content
        content3 = BeautifulSoup(html3,'html.parser')
        tr_all=content3.find('tbody').findAll('tr')
        for tr in tr_all:
            ss=tr.findAll('td')[2].find('a').get_text()
            ss=re.split(r"[()]", ss)[1]
            if(ss==token_name):
                etherscan_link='https://etherscan.io'+tr.findAll('td')[2].find('a')['href']
                driver.get(etherscan_link)
                html4 = driver.execute_script("return document.body.innerHTML;")
                content4 = BeautifulSoup(html4,'html.parser')
                #get holder and decimal
                divsummary=content4.find('div',attrs={'id':'ContentPlaceHolder1_divSummary'}).findAll('td')
                for tt in divsummary:
                    holder=tt.get_text()
                    holder=re.sub(r'\s+', '', holder)
                    if(holder=='TokenHolders:'):
                        token_holders=tt.find_next_sibling().get_text()
                        token_holders=re.sub('[:a-zA-Z\s+]', '', token_holders)
                    if ('TokenDecimals:' in holder):
                        decimal = tt.find_next_sibling().get_text()
                        decimal = re.sub('[:a-zA-Z\s+]', '', decimal)
                #get tnx_no
                if(content4.find('span',attrs={'id':'totaltxns'})) :
                   # driver.get(etherscan_link)
                    txn_no=content4.find('span',attrs={'id':'totaltxns'}).get_text()
                #get eth_add
                if(content4.find('tr',attrs={'id':'ContentPlaceHolder1_trContract'})) :
                    eth_address=content4.find('tr',attrs={'id':'ContentPlaceHolder1_trContract'}).find('a').get_text()

                #get reputation
                if(content4.find('span',attrs={'class':'pull-right repStyle'})):
                    reputation=content4.find('span',attrs={'class':'pull-right repStyle'}).find('a').get_text()
                #get token links table
                if (content4.find('tr', attrs={'id': 'ContentPlaceHolder1_tr_officialsite_2'})):
                    for offisial in content4.find('tr', attrs={'id': 'ContentPlaceHolder1_tr_officialsite_2'}).findAll('td')[1].findAll('li'):
                        token_type = offisial.find('a')['data-original-title']
                        token_type=re.split(r"[:]", token_type)[0]
                        if(token_type=='Email'):
                            token_url = re.split(r"[:]", offisial.find('a')['data-original-title'])[2]
                        else:
                            token_url = offisial.find('a')['href']
                #get twitter and facebook
                        if(token_type=='Facebook'):
                             tentative.facebook(token_url,token_name)
                        if (token_type == 'Twitter'):
                            tentative.twitter(token_url,token_name)

                for token_li in content.find('ul',attrs={'class':'list-unstyled'}).findAll('li'):
                    span_title=token_li.find('span')['title']
                    token_type=''
                    token_url=''
                    if(span_title!='Tags' and span_title!='Rank' and span_title!='Announcement'):
                        token_type=token_li.find('span').find_next_sibling().get_text()
                        token_url=token_li.find('span').find_next_sibling()['href']
                        x.execute(
                            "INSERT INTO token_links(token,link_types,url) VALUES (%s,%s,%s)",
                            (token_name, token_type, token_url))
                        conn.commit()
                x.execute(
                    "INSERT INTO tokens(token,platform,announcement,rank,cap_usd,cap_btc,cap_eth,volume_usd,volume_btc,volume_eth,total_supply,max_supply,git_name,git_desc,location,git_repos,git_people,git_languages,git_topics,token_holders,txn_no,eth_address,decimals,reputation,tag,circulating_supply) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (token_name, platform, anno, rank, cap_usd, cap_btc, cap_eth, volume_usd, volume_btc, volume_eth, total_supply, max_supply,
                     git_name, git_des, location, git_repos, git_people, git_languages, git_topic,token_holders,txn_no,eth_address,decimal,reputation,token_tags,circulating_supply))
                conn.commit()




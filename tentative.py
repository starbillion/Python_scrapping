from selenium import webdriver
import re
from bs4 import BeautifulSoup
import mysql.connector
conn = mysql.connector.connect(host='localhost',database='src',user='root',password='')
x = conn.cursor()
driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
def twitter(url,token):
    driver.get(url)
    #driver.execute_script("window.scrollTo(0,30000);")
    html2 = driver.execute_script("return document.body.innerHTML;")
    content = BeautifulSoup(html2,'html.parser')

    if(content.find('ol',attrs={'id':'stream-items-id'})):
        for twiter in content.find('ol',attrs={'id':'stream-items-id'}).findAll('li',attrs={'data-item-type':'tweet'}):
            name = ''
            time = ''
            total_content = ''
            twwet_content=''
            adap_img=''
            quote=''
            quote_img=''
            if(twiter.find('strong',attrs={'class':'fullname show-popup-with-id u-textTruncate '})):
                name=twiter.find('strong',attrs={'class':'fullname show-popup-with-id u-textTruncate '}).get_text()
                time=twiter.find('strong',attrs={'class':'fullname show-popup-with-id u-textTruncate '}).parent.parent.find_next_sibling().find('a')['title']
                if(twiter.find('p', attrs={'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'})):
                    twwet_content=twiter.find('p', attrs={'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'}).get_text()
                # if (twiter.find('div',attrs={'class':'card2 js-media-container '})):
                #     print (twiter.find('div', attrs={'class': 'card2 js-media-container '}))
                #     if (twiter.switch_to.frame('xdm_default6098_provider')):
                #         print(twiter.switch_to.frame('xdm_default6098_provider'))
                #
                #     # if(twiter.find('div',attrs={'class':'card2 js-media-container '}).find('iframe')):
                #     #     iframe=twiter.find('div',attrs={'class':'card2 js-media-container '}).find('iframe')['src']
                #     #     driver.get(iframe)
                #     #     html3 = driver.execute_script("return document.body.innerHTML;")
                #     #     content_iframe = BeautifulSoup(html3, 'html.parser')
                #     #     if(content_iframe.find('img')):
                #     #         img2=content_iframe.find('img')['src']

                if (twiter.find('div',attrs={'class':'AdaptiveMediaOuterContainer'})):
                    if(twiter.find('div',attrs={'class':'AdaptiveMediaOuterContainer'}).find('img')):
                        adap_img=twiter.find('div',attrs={'class':'AdaptiveMediaOuterContainer'}).find('img')['src']
                if (twiter.find('div',attrs={'class':'QuoteTweet-container'})):
                    quote=twiter.find('div',attrs={'class':'QuoteTweet-container'}).get_text()
                    if (twiter.find('div', attrs={'class': 'QuoteTweet-container'}).find('img')):
                        quote_img=twiter.find('div', attrs={'class': 'QuoteTweet-container'}).find('img')['src']

                total_content=twwet_content+adap_img+quote+quote_img
            comments=twiter.find('div',attrs={'class':'ProfileTweet-action ProfileTweet-action--reply'}).find('span',attrs={'class':'ProfileTweet-actionCountForPresentation'}).get_text()
            shares = twiter.find('div', attrs={'class': 'ProfileTweet-action ProfileTweet-action--retweet js-toggleState js-toggleRt'}).find('span', attrs={'class': 'ProfileTweet-actionCountForPresentation'}).get_text()
            likes = twiter.find('div', attrs={'class': 'ProfileTweet-action ProfileTweet-action--favorite js-toggleState'}).find('span', attrs={'class': 'ProfileTweet-actionCountForPresentation'}).get_text()

            x.execute(
                "INSERT INTO twitter (tokens,user_name,times,content,share,likes,comment) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (token, name, time, total_content, shares, likes, comments))
            conn.commit()
def facebook(url,token):
    url=url+'posts'
    driver.get(url)
    # driver.execute_script("window.scrollTo(0,30000);")
    html2 = driver.execute_script("return document.body.innerHTML;")
    content = BeautifulSoup(html2, 'html.parser')

    if (content.findAll('div', attrs={'class': '_5pcr userContentWrapper'})):
        for body in content.findAll('div', attrs={'class': '_5pcr userContentWrapper'}):
            share = '0'
            content1 = ''
            content2 = ''
            content = ''
            img_url = ''
            likes = ''
            likes_count = ''
            comment_str = ''
            comment = ''
            comment_count = ''
            # get name
            name = body.find('span', attrs={'class': 'fwn fcg'}).find('a').get_text()
            # get post time
            time = \
            body.find('div', attrs={'class': '_5pcp _5lel'}).find('span', attrs={'class': 'fsm fwn fcg'}).find('abbr')[
                'title']
            # get post content
            if (body.find('div', attrs={'class': '_5pbx userContent'})):
                content1 = body.find('div', attrs={'class': '_5pbx userContent'}).get_text()
            if (body.find('div', attrs={'class': '_3x-2'})):
                content2 = body.find('div', attrs={'class': '_3x-2'}).get_text()
                if (body.find('div', attrs={'class': '_3x-2'}).findAll('img')):
                    for img in body.find('div', attrs={'class': '_3x-2'}).findAll('img'):
                        img_url = img_url + img['src']
            content = content1 + content2 + img_url
            # get likes
            if (body.find('div', attrs={'class': 'UFIList'})):
                likes = body.find('div', attrs={'class': 'UFIList'}).find('div',
                                                                          attrs={'class': 'UFILikeSentenceText'}).find(
                    'span').get_text()
                likes_str = re.split(r"[,]", likes)
                like_num = re.findall('\d+', likes)
                likes_count = len(likes_str) + int(like_num[0]) - 1
                # get comment
                if (body.find('div', attrs={'class': 'UFIRow UFIPagerRow _4oep _48pi'})):
                    comment_str = body.find('a', attrs={'class': 'UFIPagerLink'}).get_text()
                    comment = re.findall('\d+', comment_str)
                    if (body.findAll('div', attrs={'aria-label': 'Comment'})):
                        j = 0
                        for i in body.findAll('div', attrs={'aria-label': 'Comment'}):
                            j = j + 1;
                    comment_count = int(comment[0]) + j
            # get share counts
            if (body.find('div', attrs={'class': 'uiUfi UFIContainer _5pc9 _5vsj _5v9k'})):
                if (body.find('div', attrs={'class': 'UFIRow UFIShareRow'})):
                    share = body.find('div', attrs={'class': 'UFIRow UFIShareRow'}).find('a').get_text()
                    share = re.sub('[:a-zA-Z]', '', share)
            x.execute(
                "INSERT INTO facebook (token,user_name,times,content,share,likes,comment) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (token, name, time, content, share, likes_count, comment_count))
            conn.commit()




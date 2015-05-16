__author__ = 'p'
import requests
import mysql.connector
from bs4 import BeautifulSoup
import re
connection_config = {'user': 'root',
                     'password': '12345678',
                     'host': '127.0.0.1',
                     'database': 'wxhyzh'}

class BookDownloadInfo(object):
    def __init__(self, furl, name, type, size):
        self.url = furl
        self.key = furl.split('=')[1]
        self.name = name
        self.type = type
        self.size = size
    def __str__(self):
        return '书名:'+self.name+'\n'+self.type+'\n相关信息:'+self.size+'\nkey:'+self.key

def getShortUrl(url):
    dburl = 'http://dwz.cn/create.php'
    data = {
        'url': url
    }
    r = requests.post(dburl, data=data)
    json = r.json()
    print(json)
    return json['tinyurl']

def bindUserEmail(openid, email):
    con = mysql.connector.connect(**connection_config)
    cursor = con.cursor()
    cursor.execute('insert into emails(uid,email) VALUES ("%s", "%s")' % (openid, email))
    con.commit()
    cursor.close()
    con.close()


def isUserEmailBinded(openid):
    con = mysql.connector.connect(**connection_config)
    cursor = con.cursor()
    cursor.execute('select * from emails where uid="%s"' % openid)
    result = cursor.fetchall()
    cursor.close()
    con.close()
    if len(result) > 0:
        return True
    else:
        return False


def searchBook(book):
    url = 'https://www.mlook.mobi/search'
    param = {
        'q': book
    }
    #Cookie: a=; username=myjsy
    cookie = {
        'a': '7070KzHTkcm1Z0TvtCSpALFl5yRfTkwOgFNwFygTyDATGQVzFi1n5cbtCHd2w2bbWfJWfB%252Fqk1e2muCqwf2%252B1IpPqnOB%252F0P4F%252Bfhxs4BH2aKRA',
        'username': 'myjsy',
        'category': 'all'
    }
    header = {
        'Host': 'www.mlook.mobi',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Referer': 'https://www.mlook.mobi/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }
    result = requests.get(url, params=param, cookies=cookie, headers=header)
    #print(result.text)
    soup = BeautifulSoup(result.text, 'html5lib')
    bookLink = soup.find('a', href=re.compile('^/book/info/'))
    #print(bookLink)
    if bookLink is not None:
        bookUrl = 'https://www.mlook.mobi'+bookLink['href']
        header['Referer'] = result.url
        r = requests.get(bookUrl, headers=header, cookies=cookie)
        #print(r.text)
        soup = BeautifulSoup(r.text, 'html5lib')
        ebooks = soup.find_all('div', class_='ebook clearfix')
        bookInfos = []
        if len(ebooks) > 0:
            for x in ebooks:
                downloadLink = x.find('a', class_='download', rel='tipsy')
                bookSizeInfo = x.find('span', class_='fs12 ffgeorgia')
                stripInfo = bookSizeInfo.text.strip()
                stripInfo = stripInfo[:stripInfo.find('推送')+2]
                bookInfo = BookDownloadInfo(downloadLink['href'].strip(), downloadLink.text.strip(), downloadLink['original-title'].strip(), stripInfo)
                print(bookInfo)
                bookInfos.append(bookInfo)
        return bookInfos

if __name__ == '__main__':
    result = searchBook('天龙八部')
    for x in result:
        print(x)
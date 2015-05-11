__author__ = 'p'
import requests
import mysql.connector
from bs4 import BeautifulSoup
import re
connection_config = {'user': 'root',
                     'password': '12345678',
                     'host': '127.0.0.1',
                     'database': 'wxhyzh'}


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
        'a': '96273Ws23txhcfv%252Fo0Zzy7UQ72k1wual9SDg50EdhTiZqSQIQ%252BTehGAd16gBrJNX5Xpk6G8lmdb5KPd5ZSx3QQ18CYAHqEKGQwYCULLHOUOXPA',
        'username': 'myjsy'
    }
    header = {
        'Host': 'www.mlook.mobi',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }
    result = requests.get(url, params=param, cookies=cookie, headers=header)
    print(result.text)
    soup = BeautifulSoup(result.text, 'html5lib')
    bookLink = soup.find('a', href=re.compile('^/book/info/'))
    print(bookLink)
    if bookLink is not None:
        bookUrl = 'https://www.mlook.mobi'+bookLink['href']
        r = requests.get(bookUrl, headers=header, cookies=cookie)
        print(r.text)
if __name__ == '__main__':
    searchBook('天龙八部')
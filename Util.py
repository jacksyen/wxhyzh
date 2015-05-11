__author__ = 'p'
import requests
import mysql.connector
from bs4 import BeautifulSoup
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
    cookie = {
        'a': '4748Xa1c9%252BztLj7CiVC%252Bi7Uz%252FrYBC7bcHsfjUKLEoR1BAsu2otRn0fZ9eLxuk9XiEqEri8cGuUxfNg0TZJXfGP6ZKEVanrdqjPXmkTOGAnM4bg',
        'username': 'myjsy',
        'category': 'all'
    }
    header = {
        'Host': 'www.mlook.mobi',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
        'Referer': 'https://www.mlook.mobi/search?q=%E5%A4%A9%E9%BE%99%E5%85%AB%E9%83%A8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }
    result = requests.get(url, params=param, cookies=cookie, headers=header)

if __name__ == '__main__':
    searchBook('天龙八部')
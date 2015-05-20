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
        return '书名:' + self.name + '\n' + self.type + '\n相关信息:' + self.size + '\nkey:' + self.key

    def toString(self):
        return '书名:' + self.name + '\n' + self.type + '\n相关信息:' + self.size + '\n点击推送:\n' + self.download_url + '\n'

    def toDict(self):
        data = {'book_key': self.key, 'name': self.name, 'type': self.type, 'size': self.size}
        return data


def getShortUrl(url):
    dburl = 'http://dwz.cn/create.php'
    data = {
        'url': url
    }
    r = requests.post(dburl, data=data)
    json = r.json()
    status = json['status']
    if status == 0:
        return json['tinyurl']
    else:
        return None

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


def loginMlook():
    url = 'https://www.mlook.mobi/member/login'
    header = {
        'Host': 'www.mlook.mobi',
        'Origin': 'https://www.mlook.mobi',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Referer': 'https://www.mlook.mobi/member/login',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }
    data = {
        'f': 'https://www.mlook.mobi/',
        'person[login]': '2309623743@qq.com',
        'person[password]': 'lipan1234',
        'person[remember_me]': '0',
        'commit': '登录',
    }
    # session = requests.Session()
    s = requests.session()
    r = s.get(url=url, headers=header)
    soup = BeautifulSoup(r.text, 'html5lib')
    fh = soup.find('input', {'name': 'formhash'})
    if fh is not None:
        data['formhash'] = fh['value']

    responese = s.post(url=url, headers=header, data=data, cookies=None)
    # print(responese.status_code)
    #print(responese.request.headers)
    return s


def searchBook(book):
    url = 'https://www.mlook.mobi/search'
    param = {
        'q': book
    }
    header = {
        'Origin': 'https://www.mlook.mobi',
        'Host': 'www.mlook.mobi',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Referer': 'https://www.mlook.mobi/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }
    s = loginMlook()
    result = s.get(url=url, params=param, headers=header)
    # print(result.text)
    #print(result.request.headers)
    soup = BeautifulSoup(result.text, 'html5lib')
    booksDiv = soup.find('div', class_='books')
    bookLink = booksDiv.find('a', href=re.compile('^/book/info/'))
    print(bookLink)
    bookInfos = []
    if bookLink is not None:
        bookUrl = 'https://www.mlook.mobi' + bookLink['href']
        header['Referer'] = result.url
        r = s.get(url=bookUrl, headers=header)
        #print(r.text)
        #print(r.request.headers)
        soup = BeautifulSoup(r.text, 'html5lib')
        ebooks = soup.find_all('div', class_='ebook clearfix')

        if len(ebooks) > 0:
            for x in ebooks:
                downloadLink = x.find('a', class_='download', rel='tipsy')
                bookSizeInfo = x.find('span', class_='fs12 ffgeorgia')
                stripInfo = bookSizeInfo.text.strip()
                stripInfo = stripInfo.split(' ')[0]+stripInfo.split(' ')[1]
                bookInfo = BookDownloadInfo(downloadLink['href'].strip(), downloadLink.text.strip(),
                                            downloadLink['original-title'].strip().split('：')[1], stripInfo)
                #print(bookInfo)
                bookInfos.append(bookInfo)
    return bookInfos


if __name__ == '__main__':
    searchBook('天龙八部')
    #loginMlook()
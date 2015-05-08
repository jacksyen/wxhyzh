__author__ = 'p'
import requests


def getShortUrl(url):
    dburl = 'http://dwz.cn/create.php'
    data = {
        'url': url
    }
    r = requests.post(dburl, data=data)
    json = r.json()
    print(json)
    return json['tinyurl']

if __name__ ==  '__main__':
    getShortUrl('www.baidu.com')
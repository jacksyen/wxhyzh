__author__ = 'p'

import xml.etree.ElementTree as ET
import msgMaker
import Util
import requests
from flask import render_template
# {
# "button":[
# {
# "type":"click",
# "name":"热点文章",
#          "key":"get_random_hot_article"
#      }]
# }
BIND_EMAIL_EVENT = 'bind_email'
SEARCH_BOOK = 'search_book'

# 用户关注处理函数


def onUserSubscribed(msg):
    return msgMaker.textMsgMaker('''欢迎关注寰宇纵横！\n
    寰宇纵横是一个提供电子书推送的工具，还能聊天哦！\n
    绑定邮箱后开始体验吧。
    ''', msg['ToUserName'], msg['FromUserName'])


# 用户取消关注处理函数
def onUserUnsubscribed(msg):
    return 'success'


# 用户点击菜单处理函数
def onMenuButtonClicked(msg):
    key = msg.get('EventKey', None)
    if key is not None:
        if key == BIND_EMAIL_EVENT:
            if Util.isUserEmailBinded(msg['FromUserName']):
                return msgMaker.textMsgMaker('您已经绑定过了了邮箱！', msg['ToUserName'], msg['FromUserName'])
            else:
                longUrl = 'phomeserver.wicp.net/bindEmail?openid='+msg['FromUserName']
                shortUrl = Util.getShortUrl(longUrl)
                return msgMaker.textMsgMaker('请点击：\n'+shortUrl+'\n完成绑定邮箱', msg['ToUserName'], msg['FromUserName'])
        elif key == SEARCH_BOOK:
            if Util.isUserEmailBinded(msg['FromUserName']):
                longUrl = 'phomeserver.wicp.net/downloadBook?openid='+msg['FromUserName']
                shortUrl = Util.getShortUrl(longUrl)
                return msgMaker.textMsgMaker('请点击：\n'+shortUrl+'\n搜索书籍', msg['ToUserName'], msg['FromUserName'])

            else:
                longUrl = 'phomeserver.wicp.net/bindEmail?openid='+msg['FromUserName']
                shortUrl = Util.getShortUrl(longUrl)
                return msgMaker.textMsgMaker('尚未绑定邮箱，请点击：\n'+shortUrl+'\n完成绑定邮箱', msg['ToUserName'], msg['FromUserName'])

    else:
        return msgMaker.textMsgMaker('点错了吧!', msg['ToUserName'], msg['FromUserName'])

# 用户通过菜单跳转URL处理函数
def onMenuUrlClicked(msg):
    pass


# ------------------------------------我是分割线 ----------------------------

# 接收普通消息处理函数
def onReceiveTextMessage(msg):
    if Util.isUserEmailBinded(msg['FromUserName']):
        url = 'http://www.tuling123.com/openapi/api'
        param = {
            'key': '347cdaca5013d5696ac45798db39e06c',
            'info': msg['Content'],
            'userid': msg['FromUserName']
        }
        r = requests.get(url=url, params=param)
        json = r.json()
        return msgMaker.textMsgMaker(json['text'], msg['ToUserName'], msg['FromUserName'])
    else:
        return msgMaker.textMsgMaker('您尚未绑定推送邮箱！', msg['ToUserName'], msg['FromUserName'])


# 接收图片消息处理函数
def onReceiveImageMessage(msg):
    pass


# 语音消息
def onReceiveVoiceMessage(msg):
    pass


# 视频消息
def onReceiveVideoMessage(msg):
    pass


# 段视频消息
def onReceiveShortVideoMessage(msg):
    pass


# 链接消息
def onReceiveLinkMessage(msg):
    pass


# 用户位置消息
def onReceiveLocationMessage(msg):
    pass


EVENT_HANDLER_MAP = {
    "subscribe": onUserSubscribed,
    "unsubscribe": onUserUnsubscribed,
    "CLICK": onMenuButtonClicked,
    "VIEW": onMenuUrlClicked,
}
NORMAL_MSG_HANDLER_MAP = {
    "text": onReceiveTextMessage,
    "image": onReceiveImageMessage,
    "voice": onReceiveVoiceMessage,
    "video": onReceiveVideoMessage,
    "shortvideo": onReceiveShortVideoMessage,
    "location": onReceiveLocationMessage,
    "link": onReceiveLinkMessage
}


def dispatchMsg(msg):
    msgDict = dict()
    xml = ET.fromstring(msg)
    for x in xml.getchildren():
        msgDict[x.tag] = x.text
    if msgDict.get('MsgType', '') == 'event':
        func = EVENT_HANDLER_MAP.get(msgDict['Event'])
        print('event')
        return func(msgDict)
    elif msgDict.get('MsgType', None) in NORMAL_MSG_HANDLER_MAP:
        func = NORMAL_MSG_HANDLER_MAP.get(msgDict['MsgType'])
        return func(msgDict)

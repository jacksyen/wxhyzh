__author__ = 'p'

import xml.etree.ElementTree as ET
import msgMaker
import Util
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

# 用户关注处理函数


def onUserSubscribed(msg):
    return msgMaker.textMsgMaker('''欢迎关注寰宇纵横！
    寰宇纵横是一个提供电子书与热门文章的推送工具，
    使用寰宇纵横可以搜索到全网的电子书，热门文章（目前支持新浪博客）并推送到你的kindle，邮箱。
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

    else:
        return msgMaker.textMsgMaker('点错了吧!', msg['ToUserName'], msg['FromUserName'])

# 用户通过菜单跳转URL处理函数
def onMenuUrlClicked(msg):
    pass


# ------------------------------------我是分割线 ----------------------------

# 接收普通消息处理函数
def onReceiveTextMessage(msg):
    if Util.isUserEmailBinded(msg['FromUserName']):
        result = Util.searchBook(msg['Content'])
        info = str()
        for x in result:
            info += x.toString()
        return msgMaker.textMsgMaker(info, msg['ToUserName'], msg['FromUserName'])
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

__author__ = 'p'

import xml.etree.ElementTree as ET
# {
# "button":[
# {
# "type":"click",
#          "name":"热点文章",
#          "key":"get_random_hot_article"
#      }]
# }

# 用户关注处理函数
def onUserSubscribed(msg):
    return '欢迎关注环宇纵横！'


# 用户取消关注处理函数
def onUserUnsubscribed(msg):
    pass


# 用户点击菜单处理函数
def onMenuButtonClicked(msg):
    pass


# 用户通过菜单跳转URL处理函数
def onMenuUrlClicked(msg):
    pass


# ------------------------------------我是分割线 ----------------------------

# 接收普通消息处理函数
def onReceiveTextMessage(msg):
    return 'ok'


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
    "subscribe": onReceiveTextMessage,
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
    if msgDict.get('MsgType', None) == 'event':
        func = EVENT_HANDLER_MAP.get(msgDict['Event'])
        func(msgDict)
    elif msgDict.get('MsgType', None) in NORMAL_MSG_HANDLER_MAP:
        func = NORMAL_MSG_HANDLER_MAP.get(msgDict['MsgType'])
        func(msgDict)
__author__ = 'p'
import time
TEXT_MSG_TEMPLATE = '''
<xml>
<ToUserName>%s</ToUserName>
<FromUserName>%s</FromUserName>
<CreateTime>%s</CreateTime>
<MsgType>text</MsgType>
<Content>%s</Content>
</xml>
'''


def textMsgMaker(content, fromuser, touser):
    """

    :param content: str
    :param fromuser: str
    :param touser: str
    :return: str
    """
    return TEXT_MSG_TEMPLATE % (touser, fromuser, int(time.time()), content)

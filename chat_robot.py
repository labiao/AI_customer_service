# !/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
文件描述：基于微信公众号实现AI客服
作者：labiao
邮箱：1725089507@qq.com
时间：2019-6-29 16:06
'''

import urllib.request
import urllib.parse
import flask
import wechatpy
import json

import time,hashlib,re,requests
import xml.etree.ElementTree as ET

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

app = flask.Flask(__name__)

def get_robot_reply(question):
    '''
    函数功能：对于特定问题进行特定回复，对于其他非特定问题进行智能回复

    参数描述：
    question 聊天内容或问题

    返回值：str，回复内容
    '''
    if "你叫什么名字" in question:
        answer = "我是八级小标拉"
    elif "你多少岁" in question:
        answer = '18'
    elif "你是GG还是MM" in question:
        answer = "你猜呢"
    else:
        try:
            # 调用NLP接口实现智能回复
            params = urllib.parse.urlencode({'msg': question}).encode()     #接口参数需要进行URL编码
            req = urllib.request.Request("http://api.itmojun.com/chat_robot", params, method="POST")    #创建请求对象
            answer = urllib.request.urlopen(req).read().decode()     #调用接口（即向目标服务器发出HTTP请求，并获取服务器的）
        except Exception as e:
            answer = "AI机器人出现故障！（原因：%s）" % str(e)
    return answer


@app.route("/wx",methods=["GET", "POST"])
def weixin_handler():  
    token = "zdy" 
    signature = flask.request.args.get("signature")
    timestamp = flask.request.args.get("timestamp")
    nonce = flask.request.args.get("nonce")
    echostr = flask.request.args.get("echostr")
    try:
        #校验token
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        # 处理异常情况或忽略
        flask.abort(403)    #校验token失败，证明这条消息不是微信服务器发送过来的

    if flask.request.method == "GET":
        return echostr
    elif flask.request.method == "POST":
        # print(flask.request.data)
        # 得到xml数据
        xmlData = ET.fromstring(flask.request.stream.read())
        # 得到粉丝发送的数据类型
        msg_type = xmlData.find('MsgType').text
        if msg_type == 'text':
            ToUserName = xmlData.find('ToUserName').text
            FromUserName = xmlData.find('FromUserName').text
            Content = xmlData.find('Content').text  #得到粉丝发送的内容
            if "你叫什么" in Content:
                Content = "郑道远"
            elif "你们小组编号" in Content:
                Content = "7"
            elif "你们小组成员" in Content:
                Content = "周紫齐（组长），郑道远，陈雷，帅田，谭新宇，王文栋，徐雨洁，卢文卓"
            else:
                Content = text_reply(Content)
            reply = '''<xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[%s]]></Content>
                    </xml>'''
            response = flask.make_response(reply % (FromUserName, ToUserName, str(int(time.time())), Content ))
            response.content_type = 'application/xml'
            return response
def text_reply(msg):
    info = msg
    api_url = 'http://www.tuling123.com/openapi/api'
    api_key = '6626a1c63fcc456485a0897df43ac8bb'
    data = {"key": api_key, "info": info}
    response=requests.post(api_url,data).content
    s = json.loads(response, encoding='utf-8')  #通过json中的loads方法，将其转变成Python中的字典对象来出来
    return s['text']
if __name__ == '__main__':
    # print( get_robot_reply("你叫什么名字"))
    # print( get_robot_reply("你多少岁"))
    # print( get_robot_reply("武汉明天天气如何"))
    # print( get_robot_reply("你是男是女"))
    # print( get_robot_reply("你到底是谁"))
    # str = input("请输入聊天内容：\n")
    # while True:
    #     if "结束聊天" in str:
    #         print("聊天结束")
    #         break
    #     else:
    #         print("AI小白：",end='')
    #         print(get_robot_reply(str))
    #     str = input("请输入聊天内容：\n")
    app.run(debug=True,host="0.0.0.0",port="80")

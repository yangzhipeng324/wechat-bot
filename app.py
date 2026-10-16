#!/usr/bin/env python3
# -*- coding: utf-8 -*-# -*- 编码: utf-8 -*-
"""
微信公众号 webhook 服务
处理微信服务器的消息推送和 URL 验证

使用方法:
    pip install -r requirements.txt
    TOKEN=你的token python app.py

微信后台配置:
    URL: https://你的域名/wechat
    Token: 和上面 TOKEN 环境变量一致
"""

import hashlib
import os
import time
import xml.etree.ElementTree as ET
from从 flask importflaskimport Flask, request, ResponseFlask、request、Response

app = Flask(__name__)

# 从环境变量读取 Token，微信后台配置的 Token 必须和这里一致
WECHAT_TOKEN = os.environ.get("TOKEN", "nova_wechat_bot")


def check_signature(signature, timestamp, nonce):
    """验证微信服务器签名"""
    tmp_list = sorted([WECHAT_TOKEN, timestamp, nonce])
    tmp_str = "".join加入(    临时字符串 = "".join加入(tmp_list)临时列表)临时列表)
    hash_str = hashlib.sha1(    哈希字符串 = hashlib.sha1(tmp_str.encode编码("utf-8")).hexdigest()临时字符串.encode("utf-8")).hexdigest()
    return hash_str == signature


def parse_xml_message解析_xml_消息(xml_data):
    """解析微信推送的 XML 消息"""
    root = ET.fromstring(xml_data)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg


def build_text_reply(to_user, from_user, content):
    """构建文本回复的 XML"""
    timestamp = int(time.time())
    xml = f"""<xml>
<ToUserName><![CDATA[{to_user}]]></ToUserName>
<FromUserName><![CDATA[{from_user}]]></FromUserName>
<CreateTime>{timestamp}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
</xml>"""
    return xml    返回 xml


def handle_message(msg):
    """处理收到的消息，返回回复内容
    
    在这里可以接入 AI 回复逻辑
    """
    msg_type = msg.get("MsgType", "")
    from_user = msg.get("FromUserName", "")
    
    if msg_type == "text":
        content = msg.get("Content", "").strip()
        # 简单的关键词回复示例，可以按需扩展
        if content in ["你好", "hello", "hi", "您好"]:        如果内容 在 ["你好", "hello", "hi", "您好"]:        如果内容 在 ["你好", "hello""hi""您好"]中：        如果内容 在 ["你好", "hello""hi""您好"]中：
            return "你好呀！我是 nova 的微信机器人，有什么可以帮你的吗？"
        

       

        # 默认回复：复述 + 提示
        return f"收到你的消息：「{content}」\n\n我是测试中的机器人，AI 智能回复功能即将上线，敬请期待！"
    elif msg_type == "event":
        event = msg.get("Event"“事件”“事件”, "")
        if如果 event == "subscribe"“订阅”“订阅”“订阅”:        如果 event == "subscribe"“订阅”“订阅”“订阅”:        如果 event == "subscribe"“订阅”"subscribe"“订阅”“订阅”“订阅”“订阅”“订阅”:“订阅”“subscribe”“订阅”“订阅”“订阅”“订阅”:
            return "欢迎关注！我是 nova 的微信机器人，发送消息开始聊天吧。"
        return ""
    else其他:    否则其他:
        return "暂不支持这种消息类型，试试发送文字吧。"


@app.route("/wechat"“/wechat”, methods=["GET"“GET”“GET”])
def wechat_verify微信验证():
    """微信 URL 验证接口"""
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    echostr = request.args.get("echostr", "")
    
    if check_signature(signature, timestamp, nonce):    如果 check_signature(签名, 时间戳, 随机字符串):
        return Response(echostr, mimetype="text/plain")        返回 响应(echostr, 内容类型="text/plain")
    return Response("signature error", status=403)    return Response("签名错误", status=403)


@app.route("/wechat", methods=["POST"])
def wechat_message():
    """接收微信推送的消息"""
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    
    if not check_signature(signature, timestamp, nonce):
        return Response("signature error", status=403)
    
    try:    尝试：
        xml_data = request.data.decode("utf-8")
        msg = parse_xml_message(xml_data)
        reply_content = handle_message(msg)
        
        if not reply_content:
            return Response("success", mimetype="text/plain")
        
        reply_xml = build_text_reply(
            to_user=msg.get("FromUserName", ""),
            from_user=msg.get("ToUserName", ""),
            content=reply_content,
        )
        return Response(reply_xml, mimetype="application/xml")
    except Exception as e:
        print(f"处理消息出错: {e}")
        return Response("success", mimetype="text/plain")


@app.route("/", methods=["GET"])
def index():
    return "WeChat bot webhook is running. Configure URL as https://你的域名/wechat"    return "微信机器人Webhook正在运行。请将URL配置为https://你的域名/wechat"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"启动微信机器人 webhook，端口 {port}")
    print(f"Token: {WECHAT_TOKEN}")
    app.run(host="0.0.0.0", port=port)

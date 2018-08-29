#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time,json
import  re
import itchat
from itchat.content import *
import sys,urllib,importlib
importlib.reload(sys)

opFlag=0				#发消息给filehelper(文件助手) open:开启 close:关闭
nAIRoom={}
nAIFriend={}
fMap={'六道':''}		#控制私聊是否回复
rMap={'群聊名称':''}   	#控制群里是否回复

# 图灵机器人请求及回复
def get_response(info,uuid):
	url = "http://www.tuling123.com/openapi/api" 
	data = {u"key":"14dddf1374cb4c43866c662865a07242", "info":info, u"loc":"", "userid":uuid}
	url2 = urllib2.Request(url,urllib.urlencode(data))
	apicontent = urllib2.urlopen(url2).read()
	rinfo = json.loads(apicontent,encoding="utf-8")
	return rinfo

@itchat.msg_register([TEXT],isGroupChat=True)
def group_reply_text(msg):
	#if msg["IsAt"] and msg["FromUserName"] in nAIRoom..keys():
	info = msg["Text"].encode("utf-8")
	chid = msg["FromUserName"].encode("utf-8")
	uuid = msg["ActualNickName"].encode("utf-8")
	#print(chid.decode()+"@"+uuid.decode()+": "+info.decode())
	with open('chat.txt', 'a') as fw:
		fw.write("群组@"+uuid.decode()+": "+info.decode()+"\n")
	fw.close()

	#if opFlag==1 and msg["IsAt"] and msg["FromUserName"] in nAIRoom.keys():
	if opFlag==1 and msg["IsAt"]:
		rinfo = get_response(info,uuid)
		if rinfo["code"] == 100000:
			rmsg="@"+uuid+" "+rinfo["text"]
			itchat.send(rmsg, chid)

@itchat.msg_register([TEXT])
def text_reply(msg):
	global opFlag
	if msg['ToUserName'] == "filehelper":
		if msg["Text"] == "open":
			itchat.send("消息助手已开启","filehelper")
			opFlag=1
		if msg["Text"] == "close":
			itchat.send("消息助手已关闭","filehelper")
			opFlag=0
		return 
	info = msg["Text"].encode("utf-8")
	chid = msg["FromUserName"].encode("utf-8")
	with open('chat.txt', 'a') as fw:
		fw.write("个人@"+chid.decode()+": "+info.decode()+"\n")
	fw.close()
	if opFlag==1 and msg["FromUserName"] not in nAIFriend.keys():
		rinfo = get_response(info,chid)
		if rinfo["code"] == 100000:
			itchat.send(rinfo["text"], chid)

itchat.auto_login(enableCmdQR=2,hotReload=True)
frlist=itchat.get_friends(update=True)
chlist=itchat.get_chatrooms(update=True)
for item in chlist:
	if item['NickName'] in rMap.keys():
		nAIRoom[item['UserName']]=item['NickName']
for item in frlist:
	if item['NickName'] in fMap.keys():
		nAIFriend[item['UserName']]=item['NickName']
itchat.run(debug=True)


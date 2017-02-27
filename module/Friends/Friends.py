#coding=utf-8
import requests
import json
import os
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.abspath('..'))
from Logger.logger import Logger
from Config.config import *
import sqlite3

class Friends(object):
    def __init__(self, cookies, uin, vfwebqq):
        self.logger = Logger('Friends')
        self.db = sqlite3.connect(DB_CONFIG['SQLITE'])
        self.target = 'http://s.web2.qq.com/api/get_user_friends2'
        self.cookies = json.loads(cookies)
        self.header = {
            'origin': 'https://d1.web2.qq.com',
            'referer': 'https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1'
        }
        self.hash = self.friendsHash(uin, self.cookies['ptwebqq'])
        self.data = {
            'r': '{"vfwebqq":"'+vfwebqq+'","hash":"'+self.hash+'"}'
        }
        self.logger.info('清理过期数据')
        query = "delete from categories"
        self.db.execute(query)
        query = "delete from friends"
        self.db.execute(query)
        self.db.commit()
        self.getFriend()

    def getFriend(self):
        result = requests.post(self.target, headers=self.header, cookies=self.cookies, data=self.data)
        jresult = json.loads(result.text)
        if jresult['retcode'] == 0:
            self.logger.info('正在获取好友分组中')
            categories = jresult['result']['categories']
            query = "insert into categories(groupId,name)values( ? , ? )"
            for i in categories:
                values = (i['index'], i['name'])
                try:
                    self.db.execute(query, values)
                except Exception as e:
                    self.logger.error(e)
            self.db.commit()
            self.logger.info('获取好友分组成功')
            self.logger.info('开始获取好友列表')
            friends = jresult['result']['friends']
            query = "insert into friends(uin,groupid)values(? , ?)"
            for x in friends:
                values = (x['uin'], x['categories'])
                try:
                    self.db.execute(query, values)
                except Exception as e:
                    self.logger.error(e)
                    self.logger.debug('0')
            self.db.commit()
            self.logger.info('获取好友列表成功，正在处理好友数据')
            marknames = jresult['result']['marknames']
            query = "update friends set markname = ? where uin = ?"
            for j in marknames:
                uin = j['uin']
                markname = j['markname']
                values = (markname, uin)
                try:
                    self.db.execute(query, values)
                except Exception as e:
                    self.logger.error(e)
                    self.logger.debug('1')
            self.db.commit()
            info = jresult['result']['info']
            query = "update friends set nickname = ? where uin = ?"
            for k in info:
                uin = k['uin']
                nickname = k['nick']
                values = (nickname, uin)
                try:
                    self.db.execute(query, values)
                except Exception as e:
                    self.logger.error(e)
                    self.logger.debug('2')
            self.db.commit()
            self.logger.info('数据处理完毕')

    def friendsHash(self, uin, ptwebqq):
        N = [0, 0, 0, 0]
        for t in range(len(ptwebqq)):
            N[t % 4] ^= ord(ptwebqq[t])
        U = ["EC", "OK"]
        V = [0, 0, 0, 0]
        V[0] = int(uin) >> 24 & 255 ^ ord(U[0][0])
        V[1] = int(uin) >> 16 & 255 ^ ord(U[0][1])
        V[2] = int(uin) >> 8 & 255 ^ ord(U[1][0])
        V[3] = int(uin) & 255 ^ ord(U[1][1])
        U = [0, 0, 0, 0, 0, 0, 0, 0]
        for T in range(8):
            if T % 2 == 0:
                U[T] = N[T >> 1]
            else:
                U[T] = V[T >> 1]
        N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        V = ""
        for T in range(len(U)):
            V += N[U[T] >> 4 & 15]
            V += N[U[T] & 15]
        return V


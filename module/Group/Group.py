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

class Group(object):
    def __init__(self, cookies, uin, vfwebqq):
        self.logger = Logger('Group')
        self.db = sqlite3.connect(DB_CONFIG['SQLITE'])
        self.target = 'http://s.web2.qq.com/api/get_group_name_list_mask2'
        self.cookies = json.loads(cookies)
        self.header = {
            'Host': 's.web2.qq.com',
            'origin': 'http://s.web2.qq.com',
            'referer': 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
        }
        self.hash = self.friendsHash(uin, self.cookies['ptwebqq'])
        self.data = {
            'r': '{"vfwebqq":"' + vfwebqq + '","hash":"' + self.hash + '"}'
        }
        self.logger.info('清理过期群组数据')
        query = "delete from groups"
        self.db.execute(query)
        self.db.commit()
        self._getGroup()

    def _getGroup(self):
        self.logger.info('获取群组列表')
        result = requests.post(self.target, cookies=self.cookies, headers=self.header, data=self.data)
        jresult = json.loads(result.text)
        if jresult['retcode'] == 0:
            query = "insert into groups(name,gid,code)values(? , ? , ?)"
            gnamelist = jresult['result']['gnamelist']
            for k in gnamelist:
                values = (k['name'], k['gid'], k['code'])
                try:
                    self.db.execute(query, values)
                except Exception as e:
                    self.logger.error(e)
            self.db.commit()
        self.logger.info('获取群组列表结束')

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
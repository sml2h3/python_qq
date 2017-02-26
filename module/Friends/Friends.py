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
        # self.db = sqlite3.connect(DB_CONFIG['SQLITE'])
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
        self.getFriend()

    def getFriend(self):
        result = requests.post(self.target, headers=self.header, cookies=self.cookies, data=self.data)
        print result.text

    def friendsHash(self, uin, ptwebqq):
        N = [0, 0, 0, 0]
        # print(N[0])
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
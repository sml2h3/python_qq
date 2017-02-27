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

class Heart(object):
    def __init__(self, cookies, psessionid):
        self.target = 'https://d1.web2.qq.com/channel/poll2'
        self.header = {
            'origin': 'https://d1.web2.qq.com',
            'referer': 'https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1'
        }
        self.psessionid = psessionid
        self.cookies = json.loads(cookies)
        self.data = {
            'r': '{"ptwebqq":"'+self.cookies['ptwebqq']+'","clientid":53999199,"psessionid":"'+self.psessionid+'","key":""}'
        }
        self.logger = Logger('Heart')
        while True:
            self.poll()
            time.sleep(1.5)


    def poll(self):
        result = requests.post(self.target, cookies=self.cookies, headers=self.header, data=self.data)
        if result.status_code == 200:
            jresult = json.loads(result.text)
            # if jresult['retcode'] != 0:
            if jresult['retcode'] != 0:
                print self.cookies
            self.logger.info(result.text)



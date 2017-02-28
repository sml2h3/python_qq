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
from Say.Say import Say


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
            'r': json.dumps({
                'ptwebqq': self.cookies['ptwebqq'],
                'clientid': 53999199,
                'psessionid': self.psessionid
            })
        }
        self.logger = Logger('Heart')
        while True:
            self.poll()
            time.sleep(1.5)

    def poll(self):
        result = requests.post(self.target, cookies=self.cookies, headers=self.header, data=self.data)
        if result.status_code == 200:
            jresult = json.loads(result.text)
            if jresult['retcode'] in (0, 116):
                if jresult['retcode'] == 0:
                    poll_type = jresult['result'][0]['poll_type']
                    result = jresult['result'][0]['value']
                    if poll_type == 'message':
                        #个人消息
                        from_uin = result['from_uin']
                        msg_id = result['msg_id']
                        to_uin = result['to_uin']
                        msg_type = result['msg_type']
                        msgtime = result['time']
                        content = result['content'][1]
                        msg_info = {
                            'poll_type': poll_type,
                            'from_uin': from_uin,
                            'msg_id': msg_id,
                            'to_uin': to_uin,
                            'msg_type': msg_type,
                            'content': content,
                            'time': msgtime
                        }
                        Say(msg_info)
                        return ''
                    elif poll_type == 'group_message':
                        #群组消息
                        from_uin = result['from_uin']
                        msg_id = result['msg_id']
                        to_uin = result['to_uin']
                        msg_type = result['msg_type']
                        msgtime = result['time']
                        content = result['content'][1]
                        group_code = result['group_code']
                        send_uin = result['send_uin']
                        msg_info = {
                            'poll_type': poll_type,
                            'from_uin': from_uin,
                            'msg_id': msg_id,
                            'to_uin': to_uin,
                            'msg_type': msg_type,
                            'content': content,
                            'time': msgtime
                        }
                        Say(msg_info)
                        return ''
            else:
                self.logger.warning('心跳包错误提示:'+jresult['retcode'])




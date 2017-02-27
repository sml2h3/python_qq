#coding=utf-8
import os
import sys
sys.path.append(os.path.abspath('module'))
from Logger.logger import Logger
from Login.Login import Login
from Heart.Heart import Heart
from Friends.Friends import Friends
from Group.Group import Group
import threading
reload(sys)
sys.setdefaultencoding('utf-8')
import json


class ControlCenter(object):
    def __init__(self):
        self.logger = Logger('ControllerCenter')
        self.logger.info('#################################################################')
        self.logger.info("#欢迎来到sml2h3的QQ机器人，下面是我的菜单，请回复菜单编号后回车 #")
        self.logger.info("#作者:sml2h3 Github:https://github.com/sml2h3                   #")
        self.logger.info("#作者博客:https://www.fkgeek.com                                #")
        self.logger.info("#1、启动QQ机器人                                                #")
        self.logger.info('#2、访问作者博客                                                #')
        self.logger.info('#################################################################')
        flag = True
        while flag:
            command = raw_input('>>')
            if command == '1':
                flag = False
                self._run()

    def _run(self):
        login_result = self._login()
        if login_result['result'] == '0':
            #启动心跳包
            cookies = json.dumps(login_result['cookies'])
            heart_thread = threading.Thread(target=self._heart, args=(cookies, login_result['psessionid']))
            getfriend_thread = threading.Thread(target=self._friend, args=(cookies, login_result['uin'], login_result['vfwebqq']))
            getgroup_thread = threading.Thread(target=self._group,
                                                args=(cookies, login_result['uin'], login_result['vfwebqq']))
            heart_thread.start()
            getfriend_thread.start()
            getgroup_thread.start()
        else:
            self.logger.error(login_result['reason'])

    def _login(self):
        return Login().run()

    def _heart(self, cookies, psessionid):
        Heart(cookies, psessionid)
        #心跳包，请用线程启动

    def _friend(self, cookies, uin, vfwebqq):
        Friends(cookies, uin, vfwebqq)

    def _group(self, cookies, uin, vfwebqq):
        Group(cookies, uin, vfwebqq)


if __name__ == '__main__':
    ControlCenter()
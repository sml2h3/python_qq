#coding=utf-8
import requests
import json
import qrcode_terminal
import os
import sys
sys.path.append(os.path.abspath('..'))
from Logger.logger import Logger
import time
reload(sys)
sys.setdefaultencoding('utf-8')


class Login(object):
    def __init__(self):
        self.login_get_cookies_url = "https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001"
        self.get_ptqrshow = "https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.9142399367333609"
        self.check = "https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken={ptqrtoken}&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-32750&mibao_css=m_webqq&t=undefined&g=1&js_type=0&js_ver=10197&login_sig=&pt_randsalt=0"
        self.code = open('code.png', 'w')
        self.jm = "http://jiema.wwei.cn/fileupload/index/op/jiema.html"
        self.logger = Logger('Login')
        self.getvfwebqq = "http://s.web2.qq.com/api/getvfwebqq?ptwebqq={ptwebqq}&clientid=53999199&psessionid=&t=1488053293431"
        self.login2 = "http://d1.web2.qq.com/channel/login2"

    def run(self):
        #开启一个session会话用来获取基础cookies以及获取二维码及其cookies
        base = requests.session()
        #访问获取基础cookies的地址
        result = base.get(self.login_get_cookies_url)
        base_cookies = result.cookies#基础cookies
        #获取二维码图片并获取二维码cookies
        result = base.get(self.get_ptqrshow)
        ptqr_cookies = result.cookies#二维码cookies
        #将二维码图片上传解码后进行二维码生成并打印到终端
        self.code.write(result.content)
        self.code.close()
        cookies = dict(base_cookies.items() + ptqr_cookies.items())
        #进行ptqrtoken计算
        qrsig = cookies['qrsig']
        e = 0
        n = len(qrsig)
        for i in range(0, n):
            e = e + (e << 5) + ord(qrsig[i])
        ptqrtoken = 2147483647 & e
        #计算完成
        #上传二维码图片解码，然后打印二维码到控制台
        try:
            rtext = requests.post(self.jm, files={'file':open('code.png', 'rb')})
        except Exception as e:
            self.logger.debug('upload qcord error')
        if rtext.status_code == 200:
            try:
                jtext = json.loads(rtext.text)
            except ValueError as e:
                self.logger.error('二维码解析返回不正常')
                exit()
            self.logger.info('请扫描屏幕中的二维码')
            url = jtext['jiema']
            #将二维码打印到控制台
            qrcode_terminal.draw(url)
            #循环验证二维码状态
            l = 0
            k = 0
            j = 0
            while True:
                result = requests.get("https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken=" + str(
                    ptqrtoken) + "&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-32750&mibao_css=m_webqq&t=undefined&g=1&js_type=0&js_ver=10197&login_sig=&pt_randsalt=0",
                                      cookies=cookies)
                if '二维码未失效' in result.text:
                    if l == 0:
                        self.logger.info('二维码未失效，等待扫码验证中')
                        l = l +1
                if '已失效' in result.text:
                    if k == 0:
                        self.logger.info('二维码已经失效')
                        k = k + 1
                        exit()
                if '认证中' in result.text:
                    if j == 0:
                        self.logger.info('二维码已被扫描，正在认证中')
                        j = j + 1
                if '登录成功' in result.text:
                    checksig_url = result.text.split("','")[2]
                    user_cookies = result.cookies
                    break
                time.sleep(1)
            #获取cookie中ptwebqq
            ptwebqq = user_cookies['ptwebqq']
            result = requests.get(checksig_url, cookies=user_cookies, allow_redirects=False)
            user2_cookies = result.cookies
            #合并两个cookies
            user3_cookies = dict(user_cookies.items()+user2_cookies.items())
            #获取vfwebqq
            headers = {
                "Referer":"http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1"
            }
            vfwebqq = requests.get(self.getvfwebqq.replace('{ptwebqq}', ptwebqq), cookies=user3_cookies, headers=headers).text
            vfwebqq = json.loads(vfwebqq)['result']['vfwebqq']
            #二次登陆，真正的登录
            data = {
                'r': '{"ptwebqq":"'+ptwebqq+'","clientid":53999199,"psessionid":"","status":"online"}'
            }
            headers = {
                'Host': 'd1.web2.qq.com',
                'Referer': 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
                'Origin':'http://d1.web2.qq.com'
            }
            result = requests.post(self.login2, data=data, cookies=user3_cookies, headers=headers)
            jresult = json.loads(result.text)
            if jresult['retcode'] == '0':
                self.logger.info('登录成功')
            else:
                self.logger.info('登录失败')
                exit()

        else:
            self.logger.error('解码发生错误,系统即将退出')
            exit()

if __name__ == '__main__':
    Login().run()
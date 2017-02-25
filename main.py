#coding=utf-8
import requests
import time


class Main(object):
    def __init__(self):
        self.login_get_cookies_url = "https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001"
        self.get_ptqrshow = "https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.9142399367333609"
        self.code = open('code.png','w')

    def login(self):
        #开启一个session会话
        login = requests.session()
        #获取基础的cookies
        result = login.get(self.login_get_cookies_url)
        base_cookies = result.cookies
        #获取二维码和二维码cookies
        result = login.get(self.get_ptqrshow)
        self.code.write(result.content)
        self.code.close()
        code_cookies = result.cookies
        cookies = dict(base_cookies.items()+code_cookies.items())
        qrsig = cookies['qrsig']
        e = 0
        n = len(qrsig)
        print n
        for i in range(0, n):
            e = e + (e << 5) + ord(qrsig[i])
        ptqrtoken = 2147483647 & e
        print ptqrtoken
        print cookies
        while True:
            result = requests.get("https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken="+str(ptqrtoken)+"&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-32750&mibao_css=m_webqq&t=undefined&g=1&js_type=0&js_ver=10197&login_sig=&pt_randsalt=0",cookies=cookies)
            print result.text
            time.sleep(1)

#ptuiCB('0','0','http://ptlogin4.web2.qq.com/check_sig?pttype=1&uin=651793701&service=ptqrlogin&nodirect=0&ptsigx=29760e89b5718498709eed2ea98443aab0c6694b6ac357f48819abcd1af48b59c41d6395f0a8f9e98dc255a827c74532a0c7123d8a200878ec9b3fddf627860a&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&f_url=&ptlang=2052&ptredirect=100&aid=501004106&daid=164&j_later=0&low_login_hour=0&regmaster=0&pt_login_type=3&pt_aid=0&pt_aaid=16&pt_light=0&pt_3rd_aid=0','0','登录成功！', 'sml2h3');




if __name__ == '__main__':
    login = Main()
    login.login()
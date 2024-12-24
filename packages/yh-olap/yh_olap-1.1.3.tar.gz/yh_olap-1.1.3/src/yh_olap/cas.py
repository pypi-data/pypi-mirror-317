import requests
import pyotp
import uuid
import logging
from tenacity import retry, stop_after_attempt, retry_if_exception_type, before_sleep_log, wait_fixed

logging.basicConfig(level=logging.INFO)


class Cas:
    def __init__(self):
        self.session = requests.Session()
        self.UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'

    def Jsessionid(self):
        jsessionid = uuid.uuid4().hex
        jsessionid = f"JSESSIONID={jsessionid[:32]}"
        jsessionid = jsessionid.upper()
        return jsessionid

    @retry(stop=stop_after_attempt(3))
    def login(self, username, password, otp_key):
        self.session = requests.Session()
        url = 'https://idaas-cas.yonghui.cn/cas/login'
        get_headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': self.UserAgent}
        post_headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': self.UserAgent}
        e1s1_data = {'flag': 1,
                     'username': username,
                     'password': password,
                     'phoneNum': None,
                     'captcha': None,
                     'sourceType': 1,
                     'execution': 'e2s1',
                     '_eventId': 'submit',
                     'geolocation': None}
        self.session.get(url=url, headers=get_headers)
        self.session.get(url=url, headers=get_headers)
        res = self.session.post(url=url, headers=post_headers, data=e1s1_data)
        id = "dynamicPassword"
        res_status_code = res.status_code
        res_text = res.text
        if res_status_code == 200:
            cookies = res.cookies
            if cookies:
                self.cookies = cookies
            else:
                raise ValueError('登录失败，未获取cookie')
        elif res_text.find('id = "dynamicPassword"'):
            dynamic_password = pyotp.TOTP(otp_key).now()
            e1s2_data = {'flag': 1,
                         'token': dynamic_password,
                         'username': username,
                         'password': None,
                         'phoneNum': None,
                         'captcha': None,
                         'sourceType': 1,
                         'execution': 'e2s2',
                         '_eventId': 'submit',
                         'geolocation': None}
            res = self.session.post(url=url, headers=post_headers, data=e1s2_data)
            if res_status_code == 200:
                cookies = res.cookies
                if cookies:
                    self.cookies = cookies
                else:
                    raise ValueError('登录失败，未获取cookie')
            else:
                raise ValueError('登录失败，未获取cookie')
        else:
            raise ValueError('登录失败，未获取cookie')

    @retry(stop=stop_after_attempt(3))
    def redirect_url(self, url):
        headers = {'User-Agent': self.UserAgent}
        res = self.session.get(
            url=f'https://idaas-cas.yonghui.cn/cas/login?service=http://cas-prod.bigdata.yonghui.cn:7070/redirect?redirectUrl={url}/',
            headers=headers)
        jsessionid = self.session.cookies.get_dict().get('JSESSIONID')
        if jsessionid:
            return jsessionid
        else:
            raise ValueError('登录失败，未获取cookie')

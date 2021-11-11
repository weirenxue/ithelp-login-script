import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import json, os, sys

if getattr(sys, 'frozen', False):
    applicationPath = os.path.dirname(sys.executable)
elif __file__:
    applicationPath = os.path.dirname(__file__)

try:
    s_account = json.load(open(os.path.join(applicationPath, "sAccount.json"), "r", encoding="utf-8"))

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}
    loginPayload = {'account': s_account['account'], 'password': s_account['password'], '_token':''}
    sess = requests.Session()
    sess.headers.update(headers)

    url = "https://member.ithome.com.tw/login"
    response = sess.get(url)
    bsObj = bs(response.text, "html.parser")
    loginToken = bsObj.find('input', {'name':'_token'}).attrs['value']
    loginPayload['_token'] = loginToken

    url = "https://member.ithome.com.tw/login"
    response = sess.post(url, data=loginPayload)
    bsObj = bs(response.text, "html.parser")
    account = bsObj.find('p', {'class': 'account-fontsize'}).get_text()
    if account == loginPayload['account']:
        url = "https://member.ithome.com.tw/oauth/authorize?client_id=ithelp&redirect_uri=https://ithelp.ithome.com.tw/users/callback&response_type=code"
        response = sess.get(url)
        
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), s_account['account'], '登入成功')
except Exception as e:
    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), s_account['account'], e, e.with_traceback)
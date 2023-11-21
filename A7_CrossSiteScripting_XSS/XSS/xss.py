import requests
import json
import logging

def run_script(url,cookie,proxy):
    headers = {
        "Cookie": cookie,
        "webgoat-requested-by": "dom-xss-vuln"
    }
    
    proxies = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    }

    burp0_data = {"param1": "42", "param2": "24"}
    response=requests.post(url, headers=headers, data=burp0_data, proxies=proxies)
    output = response.json()["output"]
    output_value = output.split("is")[1].strip()
    logging.info(f'[*] {output}')
    burp0_url = "http://127.0.0.1:8080/WebGoat/CrossSiteScripting/dom-follow-up"
    burp0_headers = {"Cookie":cookie, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "http://127.0.0.1:8080", "Connection": "close", "Referer": "http://127.0.0.1:8080/WebGoat/start.mvc", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "X-PwnFox-Color": "red"}
    burp0_data = {"successMessage": output_value}
    response=requests.post(burp0_url, headers=burp0_headers, data=burp0_data, proxies=proxies)
    json_response = json.loads(response.text)
    if json_response.get("lessonCompleted") == True:
        logging.info("[*] Challenge DOM-Based XSS validé ! :)\n")


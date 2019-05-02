import time

import requests
from setting import ua

def proxy():
    url = 'your api'
    headers = {
        'User-Agent': ua,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        ip_port = response.text.strip('\r\n')
        proxies = {
            'http': 'http://' + ip_port,
            'https': 'https://' + ip_port,
        }
        return proxies
    else:
        time.sleep(5)
        proxy()

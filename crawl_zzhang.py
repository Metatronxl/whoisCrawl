import requests
import time
import re

url = 'http://tool.chinaz.com/ipwhois?q='
headers = {
        'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

def search_ip_info(ip):

    ip_url = url + ip
    web_data = requests.get(ip_url)
    company_name = re.findall("<p>Name : (.*?)</p>",web_data.content.decode('utf-8'))


    print(company_name)


if __name__ == '__main__':
    search_ip_info('8.8.8.8')

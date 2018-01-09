# 通过http://whois.chinaz.com/网站来爬取whois信息

import requests
import time
import re
from bs4 import BeautifulSoup


url = 'http://whois.chinaz.com/'
headers = {
        'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

def search_ip_info(ip):

    ip_url = url + ip
    web_data = requests.get(ip_url)
    soup = BeautifulSoup(web_data.content,'lxml')
    registrar = soup.select('#sh_info > li:nth-of-type(2) > div.fr.WhLeList-right > div > span')[0].get_text()
    email = soup.select('#sh_info > li:nth-of-type(4) > div.fr.WhLeList-right.block.ball.lh24 > span')[0].get_text()
    phone = soup.select('#sh_info > li:nth-of-type(5) > div.fr.WhLeList-right.block.ball.lh24 > span')[0].get_text()
    creation_date = soup.select('#sh_info > li:nth-of-type(6) > div.fr.WhLeList-right > span')[0].get_text()
    expiration_date = soup.select('#sh_info > li:nth-of-type(7) > div.fr.WhLeList-right > span')[0].get_text()
    DNS = soup.select('#sh_info > li:nth-of-type(9) > div.fr.WhLeList-right')[0].get_text()

    data = {
         # "公司":company,
        # "地址":company_addr,
        "注册商":registrar,
        # "国家":country,
        "邮箱":email,
        "联系电话":phone,
        "DNS":DNS,
        "创建日期":creation_date,
        "失效日期":expiration_date,
    }
    print(data)


if __name__ == '__main__':
    search_ip_info('www.meituan.com')

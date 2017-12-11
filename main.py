import whois
import time


def dealWithWhois(data):

    company = data["org"]
    company_addr = data["address"]
    country = data["country"]
    emails = data["emails"]
    creation_date = str(data["creation_date"][0])
    expiration_date = str(data["expiration_date"][0])

    newData = {
        "公司":company,
        "地址":company_addr,
        "国家":country,
        "邮箱":emails,
        "创建日期":creation_date,
        "失效日期":expiration_date
    }
    print(newData)
if __name__ == '__main__':
    tmp = whois.whois("www.qq.com")
    dealWithWhois(tmp)
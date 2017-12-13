#使用python - whois 模块
import whois
import time


def dealWithWhois(data):

    company = data["org"]
    company_addr = data["address"]
    country = data["country"]
    emails = data["emails"]
    creation_date = str(data["creation_date"])
    expiration_date = str(data["expiration_date"])
    registrar  = data["registrar"]
    dns = data["name_servers"]
    newData = {
        "公司":company,
        "地址":company_addr,
        "注册商":registrar,
        "国家":country,
        "邮箱":emails,
        "DNS":dns,
        "创建日期":creation_date,
        "失效日期":expiration_date,

    }
    print(newData)
if __name__ == '__main__':
    tmp = whois.whois("103.37.152.41")
    dealWithWhois(tmp)
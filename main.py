#使用python - whois 模块
import whois
import time
from multiprocessing import Pool
import csv

# fp = None
fp = open('geoip_mul_test.csv','w+',newline='',encoding='utf-8')
write = csv.writer(fp)
write.writerow(('IP','company','company_addr','country','emails','creation_date','expiration_date','registrar','dns'))
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
    # print(newData)
    return newData


def get_whois_info(url):

    # fp = open('geoip_mul_{}.csv'.format(x),'w+',newline='',encoding='utf-8')
    # write = csv.writer(fp)
    try:
        tmp = whois.whois(url)
        if tmp["emails"] == "abuse@iana.org":
            print(url,": abuse ip address")

        elif tmp["emails"] is None:
            print(url,": None ip address")
        else:
            # print(url,":",tmp)
            print(url,tmp["org"],tmp["address"],tmp["country"],tmp["emails"],str(tmp["creation_date"]),str(tmp["expiration_date"]),tmp["registrar"],tmp["name_servers"])
            # write.writerow((url,tmp["org"],tmp["address"],tmp["country"],tmp["emails"],str(tmp["creation_date"]),str(tmp["expiration_date"]),tmp["registrar"],tmp["name_servers"]))
            write.writerow((url,'test'))
            result = dealWithWhois(tmp)
            return result
    except whois.parser.PywhoisError:
        print("The Registry database contains ONLY .COM, .NET, .EDU domains and Registrars.")

    time.sleep(1)



if __name__ == '__main__':

    for x in range(100,256,1):
        ip_list=[]
        # fp = open('geoip_mul_{}.csv'.format(x),'w+',newline='',encoding='utf-8')
        # write = csv.writer(fp)
        # write.writerow(('IP','company','company_addr','country','emails','creation_date','expiration_date','registrar','dns'))
        for y in range(0,256,1):
            for z in range(0,256,1):
                for k in range(0,256,1):
                    ip = '{}.{}.{}.{}'.format(x,y,z,k)
                    ip_list.append(ip)
        pool = Pool(processes=4)
        pool.map(get_whois_info,ip_list)
    fp.close()




    # get_whois_info("0.0.0.100")
    # tmp = whois.whois("192.125.71.101")
    # print(dealWithWhois(tmp))



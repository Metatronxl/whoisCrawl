#使用python - whois 模块
import whois
import time
from multiprocessing import Pool
import redis
# fp = None

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)

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
        "company":company,
        "address":company_addr,
        "registrar":registrar,
        "country":country,
        "email":emails,
        "dns":dns,
        "creation_date":creation_date,
        "expiration_date":expiration_date,

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
            print(url,"None ip address")
        else:
            # write.writerow((url,tmp["org"],tmp["address"],tmp["country"],tmp["emails"],str(tmp["creation_date"]),str(tmp["expiration_date"]),tmp["registrar"],tmp["name_servers"]))
            # write.writerow((url,'test'))
            result = dealWithWhois(tmp)
            ipDict = {}
            ipDict[url] = result
            # result = url+':'+result
            print("###write success###:",result)
            return ipDict
    except whois.parser.PywhoisError:
        print("The Registry database contains ONLY .COM, .NET, .EDU domains and Registrars.")

    time.sleep(1)

def mycallback(x):
    #判断是否为None
    if x[0] == None:
        pass
    else:
        print('write:',x)
        ip_str = list(x[0].keys())[0]
        company = list(x[0].values())[0]['company']
        address = list(x[0].values())[0]['address']
        registrar = list(x[0].values())[0]['registrar']
        country = list(x[0].values())[0]['country']
        email = list(x[0].values())[0]['email']
        dns = list(x[0].values())[0]['dns']
        creation_date = list(x[0].values())[0]['creation_date']
        expiration_date = list(x[0].values())[0]['expiration_date']
        # print('test:###',ip_str,company,address,registrar,country,email,dns,creation_date,expiration_date)
        # write.writerow(list(x))
        r.lpush(ip_str,dict(company=company,address=address,registrar=registrar,country=country,email=email,dns=dns,creation_date=creation_date,expiration_date=expiration_date))
        print("write ##",ip_str,"success!")
def getIpList(file,amount = float("inf")):
    f = open(file,'r',encoding='utf-8')
    ip_list = []
    count =0
    # 将所有获取的ip放入list中
    ip_str = f.read()
    for tmp in ip_str.split(','):

        if count <amount:
            ip_list.append(tmp)
            count +=1
        else:
            break

    f.close()
    ip_list = list(set(ip_list))
    return ip_list

def divideList(list):
    length = len(list)

    list0 = list[:10000]
    list1 = list[10000:20000]
    list2 = list[20000:30000]
    list3 = list[30000:40000]
    list4 = list[40000:50000]
    list5 = list[50000:60000]
    list6 = list[60000:70000]
    list7 = list[70000:80000]
    list8 = list[80000:90000]
    list9 = list[90000:100000]


if __name__ == '__main__':


    #
    # #获取去除重复值后的ip_list数量,以及控制获取的数量
    ip_list = getIpList('ip_test.txt')
    #
    tmp = ip_list[90000:100000]
    pool = Pool(processes=4)
    for temp in tmp:
        pool.map_async(get_whois_info,(temp,),callback=mycallback)
    pool.close()
    pool.join()

    # divideList(ip_list[:10000],5)

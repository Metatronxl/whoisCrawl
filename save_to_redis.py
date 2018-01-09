import redis
import csv
import json

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)

def dealWithWhois(info):
    location = info.find("\'None\'")
    info[location]
    info = info[:location]+info[location+1:location+5]+info[location+6:]
    location = info.find("\'None\'")
    info = info[:location]+info[location+1:location+5]+info[location+6:]
    # print(location)
    return info
def read_crawlInfo(num=float("inf")):
    csv_reader = csv.reader(open('ip_mul_test.csv',encoding='utf-8'))
    count = 0 # 判断是否是第一行数据
    for row in csv_reader:
        if count ==0:
            count+=1
            continue

        else:
            print(row[0])
            res_str = dealWithWhois(row[0])
            print(res_str)
            test = res_str.replace("'","\"")
            test = test.replace("None","\"None\"")
            # print(test)
            # print(type(test))
            dict= json.loads(test)
            # print(type(dict))

        count +=1

        if count > num:
            break

def read_geoipInfo(num=float("inf")):
        csv_reader = open('./Geoip/geoip_data.csv',encoding='utf-8')
        count = 0
        for row in csv_reader:
            if count==0:
                count +=1
                continue
            else:
                print(row)
                dict = json.loads(row)
                print(type(dict))

            count +=1

            if count >num:
                break

def read_dataInfo(num=float("inf")):

    csv_reader = open('./data/dns_ip.txt',encoding='utf-8')
    count= 0
    for row in csv_reader:
        dict = json.loads(row)
        ip_str = list(dict.keys())[0]
        connections = list(dict.values())[0]['connections']
        domains = list(dict.values())[0]['domains']
        connections = list(dict.values())[0]['connections']
        print("ip_str:",ip_str,"connections:",connections,"domains:",domains)


        # conn
        print(list(dict.values())[0])
        count +=1
        if count > num:
            break


if __name__ == '__main__':
    read_geoipInfo(1)
    # read_crawlInfo(4)
    # dealWithWhois('{"165.254.149.103": {"公司": None, "地址": None, "注册商": None, "国家": None, "邮箱": ["vipar@us.ntt.net", "abuse@ntt.net", "support@us.ntt.net"], "DNS": None, "创建日期": "None", "失效日期": "None"}}')
    # read_dataInfo(5)
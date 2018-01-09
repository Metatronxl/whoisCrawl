import json
import time
import redis


pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)

def readIpFromJson(file):
    f = open('ip_test.txt','w+',encoding='utf-8')

    for line in open(file,'r'):
        temp = json.loads(line)
        # print(temp)
        #temp.keys() return a set ,so turn set into a list
        print('value:',list(temp.keys())[0])
        f.write(list(temp.keys())[0])
        f.write(',')

    f.close()

def readFullInfoFromJson(file,amount):

    count= 0

    for line in open(file,'r'):
        if count<=amount:
            tmp = json.loads(line)
            print(count,':',tmp)
            count= count+1
        else:
            break
    print('read data fininsh')

def save_toRedis(file,amount= float("inf")):
    count=0
    for line in open(file,'r'):
        if count <=amount:
            line = json.loads(line)
            # print(type(line))

            ip_str = list(line.keys())[0]
            content_dict = list(line.values())[0]
            r.lpush(ip_str,content_dict)
            print('write:##',ip_str,'## success!')
            # print(line)
            count +=1
        else:
            break



if __name__ == '__main__':
    # readIpFromJson('dns_ip.txt')
    # readFullInfoFromJson('./data/dns_ip.txt',5)
    save_toRedis('./data/dns_ip.txt')

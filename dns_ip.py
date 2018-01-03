import json
import time

def readIpFromJson(file):
    f = open('ip_test.txt','w+',encoding='utf-8')

    for line in open(file,'r'):
        temp = json.loads(line)
        # print(temp)
        #temp.keys() return a set ,so turn set into a list
        print('value:',list(temp.keys())[0])
        f.writelines(list(temp.keys())[0])

    f.close()

if __name__ == '__main__':
    readIpFromJson('dns_ip.txt')
# coding=utf-8
import pygeoip
import csv
from multiprocessing import Pool
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)


#根据GeoIP的dat文件得到国家数据
def get_countr_by_addr(addr):
    city = 'GeoIPCity.dat'
    data = pygeoip.GeoIP(city)
    result =  data.country_code_by_addr(addr)
    return result
#根据GeoIP的dat文件得到所有数据
def get_record_by_addr(addr):
    city = 'GeoIPCity.dat'
    data = pygeoip.GeoIP(city)
    result =  data.record_by_addr(addr)
    return result
##根据GeoIPOrg文件得到数据
def get_org_by_addr(addr):
    data = pygeoip.GeoIP('GeoIPOrg.dat')
    result =  data.org_by_addr(addr)
    return result
##根据GeoIPISP文件得到数据
def get_isp_by_addr(addr):
    data = pygeoip.GeoIP('GeoIPISP.dat')
    result =  data.isp_by_addr(addr)
    return result
##根据GeoIPNetspeed文件得到数据
def get_netspeed_by_adr(addr):
    data = pygeoip.GeoIP('GeoIPNetspeed.dat')
    result =  data.netspeed_by_addr(addr)
    return result

def save_data_to_csv(ip):

    res = get_record_by_addr(ip)
    res_org = get_org_by_addr(ip)
    res_isp = get_isp_by_addr(ip)
    if res != None:
        newData = {
            "city":res["city"],
            "longitude":res["longitude"],
            "latitude":res["latitude"],
            "country":res["country_name"],
            "isp":res_isp,
            "org":res_org
        }
        # result_str = "city:{},latitude:{},longtitude:{},country:{},Isp:{},Org:{}".format(res["city"],res["latitude"],res["longitude"],res["country_name"],res_isp,res_org)
        ipDict={}
        ipDict[ip]=newData
        print('#####read geoip success:',ip,":",ipDict[ip])
        return ipDict
        # print(ip,res["city"],res["latitude"],res["longitude"],res["country_name"],res_isp,res_org)
        # write.writerow((ip,res["city"],res["latitude"],res["longitude"],res["country_name"],res_isp,res_org))

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

def mycallback(x):
    # 判断是否为None
    if x[0] == None:
        pass
    else:
        ip_str = list(x[0].keys())[0]
        city = list(x[0].values())[0]['city']
        longitude = list(x[0].values())[0]['longitude']
        latitude = list(x[0].values())[0]['latitude']
        country = list(x[0].values())[0]['country']
        isp = list(x[0].values())[0]['isp']
        org = list(x[0].values())[0]['org']

        #
        # print("ip:",city,country,isp,org)
        # write.writerow(list(x))
        r.lpush(ip_str,dict(city=city,longitude=longitude,latitude=latitude,country=country,isp=isp,org=org))


if __name__ == '__main__':

    # fp = open('geoip_data.csv','w+',newline='',encoding='utf-8')
    # write = csv.writer(fp)
    # write.writerow(('IP','city','latitude','postal_code','longitude','country_name','ISP','Org'))

    # print get_record_by_addr('123.125.71.116')
    # # # get_countr_by_addr('123.125.71.116')
    # print get_org_by_addr('123.125.71.116')
    # print get_isp_by_addr('123.125.71.116')
    # # get_netspeed_by_adr('123.125.71.116')

    #获取去除重复值后的ip_list数量,以及控制获取的数量
    ip_list = getIpList('../ip_test.txt')

    # for x in range(0,256,1):
    #     for y in range(0,256,1):
    #         for z in range(0,256,1):
    #             ip = '{}.{}.{}'.format(x,y,z)
    #             ip_list.append(ip)
    #
    # pool = Pool(processes=4)
    # pool.map(save_data_to_csv,ip_list)
    pool = Pool(processes=4)
    # pool.map(get_whois_info,ip_list)
    for temp in ip_list:
        pool.map_async(save_data_to_csv,(temp,),callback=mycallback)
    pool.close()
    pool.join()
    # fp.close()
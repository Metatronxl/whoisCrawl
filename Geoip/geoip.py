# coding=utf-8
import pygeoip
import csv
from Lab.mongo_deal import find,find_one,update_one_by_ip
import traceback



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

# def save_data_to_csv(csv_name):
#
#     fp = open(csv_name,'w+',newline='',encoding='utf-8')
#     write = csv.writer(fp)
#     write.writerow(('IP','city','latitude','postal_code','longitude','country_name','ISP','Org'))
#
#     ip_list=[]
#     for x in range(0,256,1):
#         for y in range(0,256,1):
#             for z in range(0,256,1):
#                 ip = '{}.{}.{}'.format(x,y,z)
#                 res = get_record_by_addr(ip)
#                 res_org = get_org_by_addr(ip)
#                 res_isp = get_isp_by_addr(ip)
#                 print(ip)
#                 if res != None:
#
#                     print (res,res_org,res_isp)
#                     write.writerow((ip,res["city"],res["latitude"],res["longitude"],res["country_name"],res_isp,res_org))


#提取pymongo的whois信息和geoip的信息

def updateDirection():
    try:
        F_IN = open('../Lab/new_ip_list.txt','r')
        ip_list = F_IN.readlines()
        for ip in ip_list:
            ip = ip.strip()
            direction_data = get_record_by_addr(ip)
            ip_set = {'ip':ip}
            result = find_one('whois_info_all',ip_set)
            # print(result['value'])

            #如果geoip数据不存在or主数据库中不存在此ip,则跳过
            if direction_data!=None and result != None:
                for whois_dic in result['value']:
                    whois_dic['latitude'] = direction_data['latitude']
                    whois_dic['longitude'] = direction_data['longitude']
                print(result['value'])
                print(result)

                # print(direction_data['latitude'],direction_data['longitude'])

                update_one_by_ip('whois_info_all',result)
                print("============")
            else:
                pass
    except Exception:
        print(traceback.format_exc())

def get_whois_info(table,query):
    list = find(table,query)
    for temp in list:
        print(temp)

if __name__ == '__main__':

    '''
{'dma_code': 504, 'area_code': 302, 'metro_code': 'Philadelphia, PA', 'postal_code': '19893', 'country_code': 'US', 'country_code3': 'USA', 'country_name': 'United States', 'continent': 'NA', 'region_code': 'DE', 'city': 'Wilmington', 'latitude': 39.56450000000001, 'longitude': -75.597, 'time_zone': 'America/New_York'}

    '''


    print get_record_by_addr('123.125.71.116')
    # # # get_countr_by_addr('123.125.71.116')
    # print get_org_by_addr('123.125.71.116')
    # print get_isp_by_addr('123.125.71.116')
    # # get_netspeed_by_adr('123.125.71.116')

    # save_data_to_csv("geoip_city.csv")
    # get_whois_info('whois_info_all',{'ip':'52.85.155.213'})

    updateDirection()
# coding=utf-8
import pygeoip
import csv




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

def save_data_to_csv(csv_name):

    fp = open(csv_name,'w+',newline='',encoding='utf-8')
    write = csv.writer(fp)
    write.writerow(('IP','city','latitude','postal_code','longitude','country_name','ISP','Org'))

    ip_list=[]
    for x in range(0,256,1):
        for y in range(0,256,1):
            for z in range(0,256,1):
                ip = '{}.{}.{}'.format(x,y,z)
                res = get_record_by_addr(ip)
                res_org = get_org_by_addr(ip)
                res_isp = get_isp_by_addr(ip)
                print(ip)
                if res != None:

                    print (res,res_org,res_isp)
                    write.writerow((ip,res["city"],res["latitude"],res["longitude"],res["country_name"],res_isp,res_org))

if __name__ == '__main__':

    # print get_record_by_addr('123.125.71.116')
    # # # get_countr_by_addr('123.125.71.116')
    # print get_org_by_addr('123.125.71.116')
    # print get_isp_by_addr('123.125.71.116')
    # # get_netspeed_by_adr('123.125.71.116')

    save_data_to_csv("geoip_city.csv")
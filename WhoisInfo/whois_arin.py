import requests
from bs4 import BeautifulSoup
import datetime
import time

def cidr_extract(netblocks):
    cidr_list = []
    for netblock in netblocks:

        cidrlength = netblock.cidrlength.text
        startaddress = netblock.startaddress.text
        cidr = '{}/{}'.format(startaddress,cidrlength)
        # print(netblock)
        # print(cidr)
        cidr_list.append(cidr)
    # print(cidr_list)
    return cidr_list

def netType_extract(netblocks):
    netType_list = []
    for netblock in netblocks:
        netType = netblock.description.text
        netType_list.append(netType)
    return netType_list

def net_range_extracrt(netblocks):
    net_range =''
    # list = '118.0.0.0 - 118.255.255.255'
    for netblock in netblocks:
        start_addr = netblock.startaddress.text
        end_addr = netblock.endaddress.text
        net_range = '{} - {}'.format(start_addr,end_addr)
    return net_range



def dealWithDate(date):

    '''
    utc -> %Y-%M_%D 暴力转换
    2007-01-17T11:02:19-05:00
    2007-01-17
    '''
    new_date = date[:10]
    return new_date


def dealWithXML(document):

    soup = BeautifulSoup(document,'lxml')
    nets = soup.find_all('net')
    # print(soup.prettify())  #获取整个xml的信息
    net_list = []

    for net in nets:
        # print(net.prettify())
        print('=============================================')
        created = net.registrationdate.text
        updated = net.updatedate.text
        handle = net.handle.text
        name = net.name
        netblocks = net.find_all('netblock')
        cidr = cidr_extract(netblocks)[0] # 获取第一个cidr值
        version = net.version.text
        netType = netType_extract(netblocks)[0] # 获取第一个netType值
        organization = net.orgref.attrs['name']
        net_range = net_range_extracrt(netblocks)
        whois_dic = {}
        whois_dic['range'] = net_range
        whois_dic['created'] = dealWithDate(created)
        whois_dic['updated'] = dealWithDate(updated)
        whois_dic['handle'] = handle
        whois_dic['name'] = name
        whois_dic['cidr'] = cidr
        whois_dic['net_type'] = netType
        whois_dic['compangy'] = organization
        whois_dic['version'] = version

        print(whois_dic)
        net_list.append(whois_dic)

    return net_list


def get_whois(url):

    res = requests.get(url)
    xml_res = res.text
    result = dealWithXML(xml_res)
    # print(xml_res)
    return result

def dealWithARIN_info(url):
    # url = '8.8.8.8'
    full_url ='https://whois.arin.net/rest/nets;q={}?showDetails=true&showARIN=false&showNonArinTopLevelNet=false&ext=netref2'.format(url)
    #print(full_url)
    value = get_whois(full_url)
    full_whois = {}
    full_whois['ip']=url
    full_whois['value']= value

    print(full_whois)

if __name__ == '__main__':

    dealWithARIN_info('8.8.8.8')




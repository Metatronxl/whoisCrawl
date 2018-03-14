import requests
from bs4 import BeautifulSoup
import datetime
import time
import traceback
from Lab.mongo_deal import  find_one,insert,add_part_date,update_part_date
from Tool.date_tool import  date_cmp

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
        # print('=============================================')
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
        whois_dic['company'] = organization
        whois_dic['version'] = version

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

    # print(full_whois)
    return full_whois

def whoisDic_update(ARIN_dic,whois_dic):
    ARIN_date = ARIN_dic['updated']
    whois_date = whois_dic['updated']

    judge_flag = date_cmp(ARIN_date,whois_date)
    if judge_flag == False:
        return judge_flag,whois_dic
    else:
        if whois_dic['created'] == ARIN_dic['created'] and \
           whois_dic['range'] == ARIN_dic['range'] and \
           whois_dic['handle'] == ARIN_dic['handle'] and \
           whois_dic['net_type'] == ARIN_dic['net_type'] and \
           whois_dic['company'] == ARIN_dic['company'] and \
           whois_dic['version'] ==  ARIN_dic['version']:
            judge_flag = False
        else:
        #更新whois数据库的数据
            whois_dic['created'] = ARIN_dic['created']
            whois_dic['range'] = ARIN_dic['range']
            whois_dic['handle'] = ARIN_dic['handle']
            whois_dic['net_type'] = ARIN_dic['net_type']
            whois_dic['company'] = ARIN_dic['company']
            whois_dic['version'] = ARIN_dic['version']
            judge_flag = True
        return judge_flag,whois_dic

def updateWhoisDB(url):

    # url = '118.244.66.189'
    ip_dict = {'ip':url}
    try:
        result = find_one('whois_info_all',ip_dict)
        ARIN_info = dealWithARIN_info(url)
        ##ARIN_info不存在,则直接pass,不更新数据库
        if ARIN_info == None:
            pass
        else:
            ARIN_value = ARIN_info['value']
            ## 当ip在数据库不存在时直接将查询更新至数据库
            if result == None:
                print(ARIN_info)
                insert('whois_info_all',ARIN_info)
                print("======")
            else:

                print(result['value'])
                result_value = result['value']
                ## 匹配数据库的操作

                ##匹配数据库中的cidr,如果不存在,则直接更新一条数据库,存在则更新数据库信息
                match_flag = False #如果匹配到了设置为True
                for arin_item in ARIN_value:
                    for result_item in result_value:
                        arin_cidr = arin_item['cidr']
                        result_cidr = result_item['cidr']
                        if arin_cidr == result_cidr:
                            match_flag = True
                            judge_flag,update_item = whoisDic_update(arin_item,result_item) ##judge_flag为False则不用更新
                            if judge_flag != False:
                                # result_item = update_item
                                update_part_date('whois_info_all',result)

                    if match_flag == True:
                        ## 数据更新
                        print(result_value)
                        print(ARIN_value)
                        match_flag = False ## 重新置为False

                    elif match_flag == False:
                        ## 插入新数据

                        print(result_value)
                        print(ARIN_value)
                        add_part_date('whois_info_all',result,arin_item)
                        print(result_value)

                # print(ARIN_info)
    except Exception as e:

        print(traceback.format_exc())



if __name__ == '__main__':

    # dealWithARIN_info('8.8.8.8')
    updateWhoisDB('118.244.66.189')

    # print(date_cmp('2017-01-17','2018-02-13'))



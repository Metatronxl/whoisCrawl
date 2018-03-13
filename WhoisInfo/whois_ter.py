import requests
from bs4 import BeautifulSoup



def cidr_extract(netblocks):
    cidr_list = []
    for netblock in netblocks:

        cidrlength = netblock.cidrlength.text
        startaddress = netblock.startaddress.text
        cidr = '{}/{}'.format(startaddress,cidrlength)
        print(netblock)
        print(cidr)
        cidr_list.append(cidr)
    # print(cidr_list)
    return cidr_list

def dealWithXML(document):

    soup = BeautifulSoup(document,'lxml')
    nets = soup.find_all('net')
    for net in nets:
        print(net.prettify())
        print('=============================================')
        created = net.registrationdate.text
        updated = net.updatedate.text
        handle = net.handle
        name = net.name
        netblocks = net.find_all('netblock')
        cidr = cidr_extract(netblocks)
        version = net.version.text
        print(version)



        # print(cidrlength)
    # print(soup.prettify())

def get_whois(url):

    res = requests.get(url)
    xml_res = res.text
    dealWithXML(xml_res)
    # print(xml_res)

if __name__ == '__main__':


    url = '8.8.8.8'
    full_url ='https://whois.arin.net/rest/nets;q={}?showDetails=true&showARIN=false&showNonArinTopLevelNet=false&ext=netref2'.format(url)
    print(full_url)
    get_whois(full_url)


import sys
import nmap


if __name__ == '__main__':
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        print('Nmap not found', sys.exc_info()[0])
        sys.exit(0)
    except:
        print('Unexpected error:', sys.exc_info()[0])
        sys.exit(0)

    print(nm.scan('172.16.30.30','22-443'))
    print(nm.scan('8.8.8.8','22-443'))
    # scan host 127.0.0.1, ports from 22 to 443
    # nm.command_line()                   # get command line used for the scan : nmap -oX – -p 22-443 127.0.0.1
    # nm.scaninfo()                       # get nmap scan informations {‘tcp': {‘services': ’22-443′, ‘method': ‘connect’}}
    # nm.all_hosts()


'''
    {'nmap': {'command_line': '/usr/local/bin/nmap -oX - -p 22-443 -sV 127.0.0.1', 'scaninfo': {'tcp': {'method': 'connect', 'services': '22-443'}}, 'scanstats': {'timestr': 'Thu Mar  8 13:37:37 2018', 'elapsed': '7.97', 'uphosts': '1', 'downhosts': '0', 'totalhosts': '1'}}, 'scan': {'127.0.0.1': {'hostnames': [{'name': 'localhost.lan', 'type': 'PTR'}], 'addresses': {'ipv4': '127.0.0.1'}, 'vendor': {}, 'status': {'state': 'up', 'reason': 'syn-ack'}, 'tcp': {22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '7.6', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/a:openbsd:openssh:7.6'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.4.28', 'extrainfo': '(Unix)', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.4.28'}}}}}
'''
import pymongo

mongo_host = '127.0.0.1'
mongo_port = 27017


try:
    db_conn = pymongo.MongoClient(mongo_host,mongo_port)
    db_cursor = db_conn.whois
except Exception as e:
    print(e)


def query_by_ip(ip):
    mongo_db = db_cursor.whois_info_all
    ip_list = mongo_db.find({"ip":ip})
    # for item in ip_list:
    #     print(item)
    return ip_list



if __name__ == '__main__':


    # print(mongo_db.count())
    # print(query_by_ip("54.255.229.96"))
    list = query_by_ip("54.255.229.96")
    for item in list:
        print(item)


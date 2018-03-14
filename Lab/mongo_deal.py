import pymongo
import sys
import traceback


MONGODB_CONFIG = {
    'host':'127.0.0.1',
    'port':27017,
    'db_name':'whois_fun_test',
    'username':None,
    'password':None
}

count = 0


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            orig = super(Singleton,cls)
            cls._instance = orig.__new__(cls,*args,**kwargs)
        return cls._instance



class MongoConn(Singleton):
    def __init__(self):
        try:
            self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'],MONGODB_CONFIG['port'])
            self.db = self.conn[MONGODB_CONFIG['db_name']]
            self.username = MONGODB_CONFIG['username']
            self.password = MONGODB_CONFIG['password']

            if self.username and self.password:
                self.connected = self.db.authenticate(self.username,self.password)
            else:
                self.connected = True

        except Exception:
            print(traceback.format_exc())
            print('Connect Statics Database Fail')
            sys.exit(1)


# try:
#     db_conn = pymongo.MongoClient(mongo_host,mongo_port)
#     db_cursor = db_conn.whois
# except Exception as e:
#     print(e)

def check_connected(conn):
    if not conn.connected:
        raise NameError+'state:connected Error'

def save(table, value):
    # 一次操作一条记录，根据‘_id’是否存在，决定插入或更新记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].save(value)
    except Exception:
        print (traceback.format_exc())

def insert(table, value):
    # 可以使用insert直接一次性向mongoDB插入整个列表，也可以插入单条记录，但是'_id'重复会报错
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].insert(value, continue_on_error=True)
    except Exception:
        print (traceback.format_exc())

def update(table, conditions, value, s_upsert=False, s_multi=False):
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        my_conn.db[table].update(conditions, value, upsert=s_upsert, multi=s_multi)
    except Exception:
        print (traceback.format_exc())

def upsert_mary(table, datas):
    #批量更新插入，根据‘_id’更新或插入多条记录。
    #把'_id'值不存在的记录，插入数据库。'_id'值存在，则更新记录。
    #如果更新的字段在mongo中不存在，则直接新增一个字段
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        bulk = my_conn.db[table].initialize_ordered_bulk_op()
        for data in datas:
            _id=data['_id']
            bulk.find({'_id': _id}).upsert().update({'$set': data})
        bulk.execute()
    except Exception:
        print (traceback.format_exc())

def upsert_one(table, data):
    #更新插入，根据‘_id’更新一条记录，如果‘_id’的值不存在，则插入一条记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        query = {'_id': data.get('_id','')}
        if not my_conn.db[table].find_one(query):
            my_conn.db[table].insert(data)
        else:
            data.pop('_id') #删除'_id'键
            my_conn.db[table].update(query, {'$set': data})
    except Exception:
        print (traceback.format_exc())

def update_one_by_ip(table,data):
    #用于补充主whois数据库的信息
    #更新插入,根据IP更新一条记录,如果ip不存在,则跳过

    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        query = {'ip':data.get('ip','')}
        if not my_conn.db[table].find_one(query):
            pass
        else:
            my_conn.db[table].update(query,{'$set':{'value':data['value']}})
    except Exception as e:
        print(e)

def update_part_date(table,data):
    # 更新数据库中过时的数据
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        query = {'ip':data.get('ip','')}
        query_res = my_conn.db[table].find_one(query)
        data_res = query_res['value']
        if data_res == None:
            data_res = []
        # data_res.append(update_data)
        new_data = data['value']
        my_conn.db[table].update(query,{'$set':{'value':new_data}})
    except Exception:
        print(traceback.format_exc())

def add_part_date(table,data,update_data):
    # 给数据的value添加新的数据
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        query = {'ip':data.get('ip','')}
        query_res = my_conn.db[table].find_one(query)
        data_res = query_res['value']
        if data_res == None:
            data_res = []
        data_res.append(update_data)
        my_conn.db[table].update(query,{'$set':{'value':data_res}})
    except Exception:
        print(traceback.format_exc())

def insert_one(table,data):
    # 将相同ip的数据放到一起


    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        query = {'ip':data.get('ip','')}
        if not my_conn.db[table].find_one(query):
            net_set = {}
            net_set['ip'] = data.get('ip','')
            net_set['value'] = []
            net_set['value'].append(data)
            my_conn.db[table].insert(net_set)
        else:
            query_res = my_conn.db[table].find_one(query)
            data_res = query_res['value']
            if data_res == None:
                data_res = []
            data_res.append(data)
            # print(data_res)
            my_conn.db[table].update(query,{'$set': {'value':data_res}})
    except Exception:
        print (traceback.format_exc())

def find_one(table, value):
    #根据条件进行查询，返回一条记录
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        return my_conn.db[table].find_one(value)
    except Exception:
        print (traceback.format_exc())


def find(table,value):
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        return my_conn.db[table].find(value)
    except Exception:
        print(traceback.format_exc())

##创建数据库索引
def createIndex(table,index):
    try:
        my_conn = MongoConn()
        check_connected(my_conn)
        print(my_conn.db[table].create_index(index))
        # print(my_conn[table].getIndexs())
    except Exception as e:
        print(e)

### 读取并存入mongo数据库中
def readFile(file):

    f_in = open(file)
    count = 0
    cal_count =0

    for file in f_in.readlines():
        file_group = file.split('\t')
        ip_str1 = file_group[0]
        ip_str2 = file_group[1]
        try:

            company_group = file_group[2]
            asn_description = file_group[3]
            ## 将str类型转成list类型
            nets = eval(file_group[4])

            for net_dict in nets:
                net_dict["ip"] = ip_str1
                net_dict["company"] = company_group
                net_dict['asn_description'] = asn_description
            # print('ip_str1:',ip_str1,'\n','ip_str2:',ip_str2,'\n','company_group:',company_group,'\n','asn_des:',asn_description,'\n','nets:',nets,'\n')
            #     net_set['ip']=ip_str1
            #     net_set['value'] = net_dict
                cal_count+=1
                print('Num:',cal_count,':',net_dict)
                # db_cursor.whois_info_all.insert(net_dict)
                insert_one('whois_info_all',net_dict)
        except Exception as e:
            print(ip_str1,nets)
            count +=1
        # 判断是否存在ip_str1和ip_str2不同的情况
        # if ip_str1!=ip_str2:
        #     print("ip_str1:",ip_str1,"\n")
        #     print("ip_str2:",ip_str2,"\n")

    print("error whois info:",count)
    f_in.close()



if __name__ == '__main__':


    # print(mongo_db.count())
    # print(query_by_ip("54.255.229.96"))

    # list = query_by_ip("54.255.229.96")
    # for item in list:
    #     print(item)
    # my_conn = MongoConn()


    list = find('whois_info_all',{'ip':'118.244.66.189'})
    for temp in list:
        print(temp)

    # createIndex('whois_info_all','ip')


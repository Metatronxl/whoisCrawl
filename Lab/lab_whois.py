
import pymongo


mongo_host = '127.0.0.1'
mongo_port = 27017


try:
    db_conn = pymongo.MongoClient(mongo_host,mongo_port)
    db_cursor = db_conn.whois
except Exception as e:
    print(e)


### 读取并存入mongo数据库中
def readFile(file):

    f_in = open(file)
    count = 0
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
                print(net_dict)
                db_cursor.whois_info_all.insert(net_dict)
        except Exception as e:
            print(ip_str1,nets)
            count +=1
        # 判断是否存在ip_str1和ip_str2不同的情况
        # if ip_str1!=ip_str2:
        #     print("ip_str1:",ip_str1,"\n")
        #     print("ip_str2:",ip_str2,"\n")

    print("error whois info:",count)
    f_in.close()

        #
        # print(file_group[0])

'''
解决asn_description中存在\t的问题
'''
def dealWithTxt(file):

    with open(file,"r",encoding="utf-8") as f:
        lines = f.readlines()
    with open("fix_result.txt","w",encoding="utf-8") as f_w:
        for line in lines:
            file_group = line.split('\t')
            ip_str1 = file_group[0]
            ip_str2 = file_group[1]
            try:
                company_group = file_group[2]
                asn_description = file_group[3]
                nets = file_group[4]
            except Exception as e:
                line = line[:-1]


            f_w.write(line)

    f.close()
    f_w.close()





if __name__ == '__main__':

    # readFile('fix_result.txt')
    # dealWithTxt('final_result.txt')


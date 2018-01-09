import redis

r = redis.Redis(host='localhost',port=6379,decode_responses=True)
r.set('name',['xixi','lidyt'])
print(r['name'])
print(r.get('name'))
print(type(r.get('name')))

# r.rpush('mylist','rpush', 'test', '1 2 3 4 5' ,'foo bar')
# # r.append('mylist','test append')
# r.delete('mylist')
# r.rpush('mylist',"{'165.254.149.103': {'公司': None, '地址': None, '注册商': None, '国家': None, '邮箱': ['vipar@us.ntt.net', 'abuse@ntt.net', 'support@us.ntt.net'], 'DNS': None, '创建日期': 'None', '失效日期': 'None'}}"
# )
print(r.lrange('mylist',0,0))
print(r.lindex('mylist',0))
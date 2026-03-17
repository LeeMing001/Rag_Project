import json
d={
    'name':"周杰伦",
    "age":11,
    "gender":"男"
}
s=json.dumps(d,ensure_ascii= False)
print("json转化",s)
print(type(s))
print(type(d))
print("字符串转行",str(d))
print('-----')
r=json.loads(s)
print(r)
print(type(r))
print('----------')
c=[{
    'name':"周杰伦",
    "age":11,
    "gender":"男"
},{
    'name':"蔡依林",
    "age":12,
    "gender":"女"
},{
    'name':"大胆儿",
    "age":1,
    "gender":"男"
}
]
ss=json.dumps(c,ensure_ascii= False)
print(ss)
print(type(ss))
print(ss[1])
tt=json.loads(ss)
print(tt)
print(tt[1])
print(type(tt))
import requests
url = "http://www.test.com/payTest"
# 发送get请求
r = requests.get(url)
# 获取返回的json数据
shuju=r.json()
print(shuju[-1].get('code'))

js_code=shuju[-1].get('code')
appid='wx04c066bae099852d'
secret='ba56b017bb62f22f2de6a5f3b9171679'
requestString='https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code'.format(APPID=appid,SECRET=secret,JSCODE=js_code)
r = requests.get(requestString)
r=r.json()
print(r['openid'])
print(r['session_key'])
return r['openid']

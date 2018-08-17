import random
import hashlib
import urllib.request
import re
import time

def get_nonce_str():
    string=[]
    for i in range(32):
        x = random.randint(1, 2)
        if x == 1:
            y = str(random.randint(0, 9))
        else:
            y = chr(random.randint(97, 122))
        string += y
        string = ''.join(string)
    return string


def trans_dict_to_xml(data):
    """
    将 dict 对象转换成微信支付交互所需的 XML 格式数据

    :param data: dict 对象
    :return: xml 格式数据
    """

    xml = []
    for k in data.keys():
        v = data.get(k)
        if k == 'detail' and not v.startswith('<![CDATA['):
            v = '<![CDATA[{}]]>'.format(v)
        xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(xml))

# urlopenid='http://localhost:3000/payTest'
# openid= urllib.request.urlopen(urlopenid).read()
# print(eval(openid.decode('utf-8'))[-1]['code'])
data = {
      'appid': 'wx04c066bae099852d',
      'mch_id': '1441169202',
      'nonce_str': get_nonce_str(),
      'body': '上链费用',                              # 商品描述
      'out_trade_no': str(int(time.time())),       # 商户订单号
    'spbill_create_ip':'127.0.0.1',  #APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
     'notify_url':' http://www.weixin.qq.com/wxpay/pay.php',  #异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数

    'trade_type': 'JSAPI',
    'total_fee':'520',
  'openid': 'o8oBc5SsQBOsISB00O81BTRnq2VM'  #（测试数据）实际从前端传过来
    # 'openid' : openid,
}
print(sorted(data))
stringA = '&'.join(["{0}={1}".format(k, data.get(k))for k in sorted(data)])
print(stringA)
merchant_key= 'interestact1tink134kaoyan5216tin'
stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
print(stringSignTemp)
stringSignTemp=stringSignTemp.encode("utf8")
sign = hashlib.md5(stringSignTemp).hexdigest().upper()

print(sign)

data['sign'] = sign
print(data)


url='https://api.mch.weixin.qq.com/pay/unifiedorder'

data=trans_dict_to_xml(data).encode('utf-8')
print(data)
req = urllib.request.Request(url=url,data=data,method='POST', headers={'Content-Type': 'application/xml'})
print(type(req))

result = urllib.request.urlopen(req, timeout=500).read()
# tree = ET.parse(result.decode('utf-8').xml)
# root = tree.getroot()
# print(root.findall('prepay_id'))
print(type(result.decode('utf-8')))
result=result.decode('utf-8')
print(result)
result=re.findall(r"<prepay_id><!\[CDATA\[(.*)]]></prepay_id>",result,re.I|re.M)
prepay_id=result[0]
# result=re.sub('<![CDATA[(.+?)]]', '', result,)
print(result[0])
# print(result.decode('utf-8'))
print(type(result))

print("prepay_id="+prepay_id)
package="prepay_id="+prepay_id
t = time.time()
data2={
     'appid': 'wx04c066bae099852d',
     'timeStamp': t,
     'nonce_str': get_nonce_str(),
     'package': package,
     'signType':'MD5',
}

stringB = '&'.join(["{0}={1}".format(k, data2.get(k))for k in sorted(data2)])
print(stringB)
stringB=stringB.encode("utf8")
paySign = hashlib.md5(stringB).hexdigest().upper()
print(paySign)


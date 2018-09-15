from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.handlers.wsgi import WSGIRequest
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from mongoengine import *
from polls.models import oath
import os

##web3
from web3 import Web3
from eth_account import Account

##Payment
import random
import hashlib
import urllib.request
import re
import time

# Create your views here.


# Define mongodb
connect('oath')

# Define os environment
env_dist = os.environ



def index(request):
    return HttpResponse('Hello,world')

def textIn(request):
    if (request.method == 'POST'):
        print('=====start=====')
        concat = request.POST
        openid = concat['openid']
        data = prepay(openid)
        return HttpResponse(data)
    return HttpResponse(False)
    # return HttpResponse(request.environ['HTTP_TEXT'])

@csrf_exempt
def prepayId(request):
    if (request.method == 'POST'):
        print('=====prepay start=====')
        concat = request.POST
        openid = concat['openid']
        data = prepay(openid)
        # print(type(data))
        data_json = json.dumps(data)
        # print(type(data_json))
        print(data_json)
        print('=====prepay start=====')
        return HttpResponse(data_json)
    return HttpResponse(False)

@csrf_exempt
def getKey(request):
    if (request.method == 'POST'):
        # print('=====getKey start=====')
        # key = env_dist['BLOCK_KEY']
        # print (key)
        # print('=====getKey end=====')
        return HttpResponse('NONE')
    return HttpResponse(False)
#
# @csrf_exempt
# def repayId(request):
#     pass

@csrf_exempt
def personId(request):
    if(request.method == 'POST'):
        print('=====start=====')
        concat = request.POST
        code = concat['code']
        print('code: '+code)
        appid = 'wx04c066bae099852d'
        secret = 'ba56b017bb62f22f2de6a5f3b9171679'
        requestString = 'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code'.format(
            APPID=appid, SECRET=secret, JSCODE=code)
        r = requests.get(requestString)
        r = r.json()
        openid = r['openid']
        print('openid: '+openid)
        print('=====end=====')
        return HttpResponse(openid)
    return HttpResponse(False)
@csrf_exempt
def personInfoIn(request):
    print('=====personInfoIn start=====')
    if(request.method == 'POST'):

        concat = request.POST
        print('concat:',concat)
        print ('text: ' + concat['text'])
        print ('username: '+concat['username'])
        text = concat['text']
        print('typestr',type(text))
        print('typeid',type(concat['openid']))
        name = concat['username']
#         tx_hash = transction(text,name)
        tx_hash=1
        docs = [
            dict(
                username=concat['username'],
                text=concat['text'],
                oathTitle=concat['oathTitle'],
                # blockNum=concat['blockNum'],
                image=concat['image'],
                time=concat['time'],
                avatarUrl=concat['avatarUrl'],
                openid=concat['openid'],
                tx_hash=tx_hash
            )
        ]
        oath_obj=oath(
#         name=concat['username'],
             name='concat['username']',
        oathText=concat['text'],
        oathTitle=concat['oathTitle'],
        image=concat['image'],
        time=concat['time'],
        avatarUrl=concat['avatarUrl'],
        openid=concat['openid'],
        tx_hash=tx_hash,
        )
        print('oath-obj',type(oath_obj))
        oath_obj.save()
        # resultList = db.update(docs)
        # updateNum = 0
        # for item in resultList:
        #     if (item[0]):
        #         updateNum += 1
        #     else:
        #         print('%s db[%s]' % (item[2], item[1]))
        # print('%s update successfully\n' % updateNum)
        # print('===has saved===')
        print('=====personInfoIn end=====')
        return HttpResponse(tx_hash)
    else:
        return HttpResponse(False)

@csrf_exempt
def personInfoOut(request):
    if(request.method == 'POST'):
        # print(request.environ)
        # for k, v in request.environ.items():
        #     print(k,v)
        print('=====personInfoOut start=====')
        concat = request.POST
        results = db.view('byWechetId/byWechetId', keys=[concat['username']])
        for row in results:
            dic = row.value
            print(dic)
        print('=====personInfoOut end=====')
        return HttpResponse(results)
    else:
        return HttpResponse(False)

def transction(text,name):
  w3=Web3(Web3.HTTPProvider('https://mainnet.infura.io/9dhHYFuxJixnXwEdnwIy '))#连接到Eth的远程节点
  priv_key = env_dist['BLOCK_KEY'] #爱链的eth账户的私钥
  account = Account.privateKeyToAccount(priv_key) #通过私钥得到公钥也就是账户地址
  nonce = w3.eth.getTransactionCount(account.address) #通) #通过返回指定地址发起的交易数，得到防止重放攻击的数字
  data=Web3.toHex(str.encode(text+'——'+name))#交易附加的信息，需要将字符串转换为16进制编码，需要前端传递来需要保存的数据
  payload = {
    'to':  '0x8Fe2Af03Ed1d362371261AB33C400F24fBB82D8f',
    'value': 0,
    'gas': 200000,           #运算步数的上限
    'gasPrice': Web3.toWei(3,'gwei'),#每一步运算耗费的Eth
    'nonce': nonce,
    'data':data
  }
  signed = account.signTransaction(payload) #打包
  # estimation = w3.eth.estimateGas(payload)
  # print(estimation)
  tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)#生成裸交易，得到交易号
  # receipt = w3.eth.waitForTransactionReceipt(tx_hash) #通过交易号得到交易的信息，一般需要等1分钟
  print('hash: '+tx_hash)
  tx_hash=''.join(['%02x'%b for b in tx_hash])
  return tx_hash

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

def prepay(openid):
    data = {
        'appid': 'wx04c066bae099852d',
        'mch_id': '1441169202',
        'nonce_str': get_nonce_str(),
        'body': '上链费用',  # 商品描述
        'out_trade_no': str(int(time.time())),  # 商户订单号
        'spbill_create_ip': '127.0.0.1',  # APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
        'notify_url': ' http://www.weixin.qq.com/wxpay/pay.php',  # 异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数
        'trade_type': 'JSAPI',
        'total_fee': '1',
        # 'openid': 'o8oBc5SsQBOsISB00O81BTRnq2VM'  # （测试数据）实际从前端传过来
        'openid' : openid,
    }
    stringA = '&'.join(["{0}={1}".format(k, data.get(k)) for k in sorted(data)])
    # print(stringA)
    merchant_key = 'interestact1tink134kaoyan5216tin'
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    # print(stringSignTemp)
    stringSignTemp = stringSignTemp.encode("utf8")
    sign = hashlib.md5(stringSignTemp).hexdigest().upper()
    data['sign'] = sign
    # print(data)

    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

    data = trans_dict_to_xml(data).encode('utf-8')
    req = urllib.request.Request(url=url, data=data, method='POST', headers={'Content-Type': 'application/xml'})
    # print(type(req))

    result = urllib.request.urlopen(req, timeout=500).read()
    # print(type(result.decode('utf-8')))
    result = result.decode('utf-8')
    # print(result)
    result = re.findall(r"<prepay_id><!\[CDATA\[(.*)]]></prepay_id>", result, re.I | re.M)
    prepay_id = result[0]  # 第一次签名传输到微信服务器获得prepay id
    # print(type(result))

    # 第二次签名，获得paySign
    package = "prepay_id=" + prepay_id
    t = time.time()
    data2 = {
        'appId': 'wx04c066bae099852d',
        'timeStamp': int(t),
        'nonceStr': get_nonce_str(),
        'package': package,
        'signType': 'MD5',
    }

    stringB = '&'.join(["{0}={1}".format(k, data2.get(k)) for k in sorted(data2)])
    stringB = '{0}&key={1}'.format(stringB, merchant_key)
    # print(stringB)
    stringB = stringB.encode("utf8")
    paySign = hashlib.md5(stringB).hexdigest().upper()
    data2['paySign'] = paySign
    # print(data2)
    # 获得paySign后，加data2字典和paySign一并传输到前端
    return data2































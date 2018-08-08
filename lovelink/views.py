from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.handlers.wsgi import WSGIRequest
import json
import requests
from django.views.decorators.csrf import csrf_exempt
import couchdb

##web3
# from web3 import Web3
# from eth_account import Account

# Create your views here.


# Define couch db
server = couchdb.Server('http://admin:admin@localhost:5984')
db = server['lovechain_test']

def index(request):
    return HttpResponse('Hello,world')

def textIn(request):
    # print(type(request))
    # print(request.environ)
    # if request.method == 'POST':
    #     form = ContactForm(request.POST)
    # for k, v in request.environ.items():
    #     print(k,v)
    # print(request.environ['HTTP_TEXT'])
    return HttpResponse(request.environ['HTTP_TEXT'])

# @csrf_exempt
# def prepayId(request):
#     pass
#
# @csrf_exempt
# def repayId(request):
#     pass

@csrf_exempt
def personId(request):
    if(request.method == 'GET'):
        print('=====start=====')
        code = request.environ['HTTP_CODE']
        appid = 'wx04c066bae099852d'
        secret = 'ba56b017bb62f22f2de6a5f3b9171679'
        requestString = 'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code'.format(
            APPID=appid, SECRET=secret, JSCODE=code)
        r = requests.get(requestString)
        r = r.json()
        print(r['openid'])
        print(r['session_key'])
        print('=====end=====')
        return r['openid']
    return HttpResponse(False)
@csrf_exempt
def personInfoIn(request):
    if(request.method == 'POST'):

        print(request.environ)
        for k, v in request.environ.items():
            print(k,v)

        concat = request.POST
        text = concat['username'] + ': ' + concat['text']
        # tx_hash = transction(text)
        docs = [
            dict(
                username=concat['username'],
                text=concat['text'],
                oathTitle=concat['oathTitle'],
                blockNum=concat['blockNum'],
                image=concat['image'],
                time=concat['time'],
                avatarUrl=concat['avatarUrl'],
                openid=concat['openid'],
                tx_hash='none'
            )
        ]
        resultList = db.update(docs)
        updateNum = 0
        for item in resultList:
            if (item[0]):
                updateNum += 1
            else:
                print('%s db[%s]' % (item[2], item[1]))
        print('%s update successfully\n' % updateNum)
        print('===has saved===')
        return HttpResponse('Person Information have saved without pay')
    else:
        return HttpResponse(False)

@csrf_exempt
def personInfoOut(request):
    if(request.method == 'POST'):

        print(request.environ)
        for k, v in request.environ.items():
            print(k,v)

        concat = request.POST
        results = db.view('byWechetId/byWechetId', keys=[concat['username']])
        for row in results:
            dic = row.value
            print(dic)
        return HttpResponse(results)
    else:
        return HttpResponse(False)

# def transction(text):
#   w3=Web3(Web3.HTTPProvider('https://mainnet.infura.io/9dhHYFuxJixnXwEdnwIy '))#连接到Eth的远程节点
#   priv_key = '5a71be5b4d5bea28a3b841f5f6a7a7a14b077cff3a82b9a02d738145a157c2fb' #爱链的eth账户的私钥
#   account = Account.privateKeyToAccount(priv_key) #通过私钥得到公钥也就是账户地址
#   nonce = w3.eth.getTransactionCount(account.address) #通过返回指定地址发起的交易数，得到防止重放攻击的数字
#   data=Web3.toHex(str.encode(text))#交易附加的信息，需要将字符串转换为16进制编码，需要前端传递来需要保存的数据
#   payload = {
#     'to': '0x8Fe2Af03Ed1d362371261AB33C400F24fBB82D8f',
#     'value': 0,
#     'gas': 200000,           #运算步数的上限
#     'gasPrice': Web3.toWei(10,'gwei'),#每一步运算耗费的Eth
#     'nonce': nonce,
#     'data':data
#   }
#   signed = account.signTransaction(payload) #打包
#   # estimation = w3.eth.estimateGas(payload)
#   # print(estimation)
#   tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)#生成裸交易，得到交易号
#   # receipt = w3.eth.waitForTransactionReceipt(tx_hash) #通过交易号得到交易的信息，一般需要等1分钟
#   print(tx_hash)
#   # print(receipt)
#   return tx_hash





























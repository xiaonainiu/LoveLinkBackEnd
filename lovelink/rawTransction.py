from web3 import Web3
from eth_account import Account

def transction(oath，name):
  w3=Web3(Web3.HTTPProvider('https://mainnet.infura.io/9dhHYFuxJixnXwEdnwIy '))#连接到Eth的远程节点
  priv_key = '5a71be5b4d5bea28a3b841f5f6a7a7a14b077cff3a82b9a02d738145a157c2fb' #爱链的eth账户的私钥
  account = Account.privateKeyToAccount(priv_key) #通过私钥得到公钥也就是账户地址
  nonce = w3.eth.getTransactionCount(account.address) #通过返回指定地址发起的交易数，得到防止重放攻击的数字wo
  words=oath+' ——'+name
  data=Web3.toHex(str.encode(words))#交易附加的信息，需要将字符串转换为16进制编码，需要前端传递来需要保存的数据
  payload = {
    'to': '0x8Fe2Af03Ed1d362371261AB33C400F24fBB82D8f',
    'value': 0,
    'gas': 200000,           #运算步数的上限
    'gasPrice': Web3.toWei(10,'gwei'),#每一步运算耗费的Eth
    'nonce': nonce,
    'data':data
  }
  signed = account.signTransaction(payload) #打包
  # estimation = w3.eth.estimateGas(payload)
  # print(estimation)
  tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)#生成裸交易，得到交易号
  receipt = w3.eth.waitForTransactionReceipt(tx_hash) #通过交易号得到交易的信息，一般需要等1分钟
  print(tx_hash)
  print(receipt)

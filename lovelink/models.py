from django.db import models
from mongoengine import *
# Create your models here.
class Oath(Document):
# oath 
meta = { 
  # 数据库中显示的名字 '
  collection': 'oath_data' } 
  openid = SequenceField(required=True, primary_key=True)
  username = StringField()
  text= StringField()
  oathTitle=StringField()
  image=StringField()
  time=StringField()
  avatarUrl=StringField()
  tx_hash=StringField()# 可以定义查询集
  @queryset_manager def show_newest(doc_cls, queryset): 
  # 通过poem_id降序显示
  return queryset.order_by('-openid') 



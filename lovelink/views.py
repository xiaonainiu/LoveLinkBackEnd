from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.handlers.wsgi import WSGIRequest
import json
import requests
from django.views.decorators.csrf import csrf_exempt
import couchdb

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

@csrf_exempt
def postRequest(request):
    if (request.method == 'POST'):
        print("the POST method")
        concat = request.POST
        # postBody = request.body
        # print(concat)
        if concat['type'] == 'save':
            data_json = json.dumps(concat)
            print(type(data_json))
            print(type(request))
            print(data_json)
            data_dict = json.loads(data_json)
            result = db.save(data_dict)
            print('===has saved===')
            # print(type(postBody))
            # print(postBody)
            return HttpResponse('has saved')
        elif concat['type'] == 'ask':
            design_doc = {
                '_id': '_design/view2',
                'views': {
                    'view2': {
                        'map': 'function(doc){emit(doc.username,doc);'
                    }
                }
            }
            results = db.view('_design/view2', keys = ['username'])
            dic = ''
            # print(type(results))
            # print(results['text'])
            # print('==========================')
            for row in results:
                dic = row.value
                print(dic)
            #
            # if len(dic) != 0:
            #     return HttpResponse('user not found')
            # else:
            #     return HttpResponse(results)
        return HttpResponse('command not found')

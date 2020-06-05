from django.shortcuts import render
from django.http import HttpResponse
from RuiNetworkApp import models
import json
import hashlib,socket
from django.db.models import Count


# Create your views here.
def index(request):
    #请求所有数据
    RuiNetWorkPortlist=models.RuiNetPorttable.objects.all()

    RuiNetWorkUserList=models.RuiNetworkUser.objects.all()
    OnlinePortSum=0
    Portnum=0
    UserName=0
    TotalFlow=0
    for i in RuiNetWorkPortlist:
        Portnum=Portnum+1
        TotalFlow=TotalFlow+int(i.PortFlow)
        if i.IsAlive !='0':
            OnlinePortSum=OnlinePortSum+1
    for i in RuiNetWorkUserList:
        UserName=UserName+1

    context={
        "OnlinePortSum":OnlinePortSum,
        "Portnum":Portnum,
        "UserName":UserName,
        "TotalFlow":TotalFlow
    }  #是一个字典
    return render(request, 'index.html',context)

def tables(request):
    RuiNetWorkPortlist = models.RuiNetPorttable.objects.all()

    context = {
        "RuiNetWorkPortlist": RuiNetWorkPortlist,
    }  # 是一个字典

    return render(request, 'tables.html', context)

def AddPort(request):
    if (request.method == 'GET'):
        PortID=request.GET.get('modport',default='-1')
        if PortID is '-1':
            ismod='0'
            RuiNetworkUserList=models.RuiNetworkUser.objects.all()
            RuiNetworkPort=None
            context = {
                'IsMod': ismod,
                'RuiNetworkPort': RuiNetworkPort,
                "RuiNetWorkUserList": RuiNetworkUserList,
            }
        else:
            RuiNetworkPort=models.RuiNetPorttable.objects.filter(id=int(PortID))
            RuiNetworkUser = models.RuiNetworkUser.objects.filter(UserID=RuiNetworkPort[0].UserID)
            RuiNetworkUserList=[RuiNetworkUser[0]]
            ismod='1'
            print(RuiNetworkPort[0].PortEndTime)
            context = {
                'IsMod': ismod,
                'RuiNetworkPort': RuiNetworkPort[0],
                "RuiNetWorkUserList": RuiNetworkUserList,
            }
            # 是一个字典
    return render(request, 'form-wizard.html',context)

def UserList(request):
    RuiNetWorkUserList = models.RuiNetworkUser.objects.all()
    context = {
        "RuiNetWorkUserList": RuiNetWorkUserList,
    }  # 是一个字典

    return render(request, 'user-list.html',context)

def NewUser(request):
    if (request.method == 'GET'):
        UserID=request.GET.get('moduser',default='-1')
        if UserID is '-1':
            ismod='0'
            RuiNetworkUser=None
        else:
            RuiNetworkUser = models.RuiNetworkUser.objects.get(id=int(UserID))

            ismod='1'
        context = {
            'IsMod':ismod,
            "RuiNetworkUser": RuiNetworkUser,
        }  # 是一个字典
    return render(request, 'new-user.html',context)


def ModUser(request):
    if (request.method == 'POST'):
        PostBody = request.body.decode('UTF-8')
        json_result = json.loads(PostBody)
        print(json_result)
        #提交的数据{'UserID': 'test', 'UserName': 'test', 'PortLimitNum': '10', 'Email': 'lelirui@8080.com', 'IsLimit': '0', 'UserDisable': '1'}
        if json_result['IsMod'] == 1:
            obj = models.RuiNetworkUser.objects.get(id=json_result['id'])
            obj.UserID=json_result['UserID']
            obj.UserName = json_result['UserName']
            obj.PortLimitNum = json_result['PortLimitNum']
            obj.Email = json_result['Email']
            obj.IsLimit = json_result['IsLimit']
            obj.UserDisable = json_result['UserDisable']
            obj.save()
            #获取端口信息如果启用，打开端口
        else:
            try:
                UserID = models.RuiNetworkUser.objects.get(UserID=json_result['UserID'])
            except:
                UserID = None
            if  UserID :
                pass
            else:
                UserIdMd5=hashlib.md5()
                UserIdMd5.update(json_result['UserID'].encode('utf-8'))  # 传入需要加密的字符串进行MD5加密
                UserKey=UserIdMd5.hexdigest()
                UserKey=UserKey[:20]
                models.RuiNetworkUser.objects.create(UserID=json_result['UserID'],UserName=json_result['UserName'],
                                                     UserOnlineStatus='0',PortInfo='',UserKey=UserKey,
                                                     IsLimit=json_result['IsLimit'],PortLimitNum=json_result['PortLimitNum'],
                                                     Email=json_result['Email'],UserDisable=json_result['UserDisable'])

    return HttpResponse(json.dumps({
                "status": 'status',
                "result": 'result'
            }))

def ModPort(request):
    #新加或者修改的数据{'CurrentPort': '2312', 'RemotePort': '12', 'RemoteIP': '127.0.0.1', 'PortEndTime': '2020-06-26', 'NetworkProtocol': 'SSH', 'ProtStatus': '1', 'UserID': 'lelirui'}
    if (request.method == 'POST'):
        PostBody = request.body.decode('UTF-8')
        json_result = json.loads(PostBody)


        if json_result['IsMod'] == 1:

            obj = models.RuiNetPorttable.objects.get(id=json_result['id'])
            # 返回过来的信息和原来的相同，不做任何处理，不同，进行操作
            try:
                NetThroughHearbeat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                NetThroughHearbeat.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                NetThroughHearbeat.connect(("127.0.0.1", 9000))
                if json_result['ProtStatus'] != obj.ProtStatus and json_result['ProtStatus'] == '1':
                    # 发送消息删除该端口
                    JsonStr = {'IsOne': False, 'EstablishPort': False, 'OpenPort': True,'ClosePort': False,
                               'CurrentPort': json_result['CurrentPort']}
                    print(JsonStr)
                    NetThroughHearbeat.send(bytes(json.dumps(JsonStr), encoding='utf-8'))
                elif json_result['ProtStatus'] != obj.ProtStatus and json_result['ProtStatus'] == '0':
                    JsonStr = {'IsOne': False, 'EstablishPort': False, 'OpenPort': False, 'ClosePort': True,
                               'CurrentPort': json_result['CurrentPort']}
                    print(JsonStr)
                    NetThroughHearbeat.send(bytes(json.dumps(JsonStr), encoding='utf-8'))
                NetThroughHearbeat.close()
            except Exception as e:
                print(e)
                print('jixu ')
                NetThroughHearbeat.close()
            obj.CurrentPort = json_result['CurrentPort']
            obj.RemotePort = json_result['RemotePort']
            obj.RemoteIP = 'cloud.pybug.cn'
            obj.PortEndTime = json_result['PortEndTime']
            obj.NetworkProtocol = json_result['NetworkProtocol']
            obj.ProtStatus = json_result['ProtStatus']
            obj.UserID=json_result['UserID']
            obj.save()

        else:
            try:
                CurrentPort=models.RuiNetPorttable.objects.get(CurrentPort=json_result['CurrentPort'])
            except:
                CurrentPort=None
            if  CurrentPort :
                return HttpResponse("failed")
            else:
                obj=models.RuiNetworkUser.objects.get(UserID=json_result['UserID'])
                portobj=models.RuiNetPorttable.objects.annotate(Count('UserID')).filter(UserID=json_result['UserID'])
                if obj.IsLimit == '1' or (obj.IsLimit == '0' and int(obj.PortLimitNum) >= len(portobj)):
                    models.RuiNetPorttable.objects.create(CurrentPort=json_result['CurrentPort'],RemotePort=json_result['RemotePort'],
                                                          NetworkProtocol=json_result['NetworkProtocol'],IsAlive='0',
                                                          PortFlow='0',ProtStatus=json_result['ProtStatus'],
                                                          RemoteIP=json_result['RemoteIP'],CurrentIP='cloud.pybug.cn',
                                                          UserID=json_result['UserID'],PortEndTime=json_result['PortEndTime'])
                    if obj.PortInfo:
                        obj.PortInfo = json_result['CurrentPort'] + '->' + json_result[
                            'RemotePort']
                    else:
                        obj.PortInfo=obj.PortInfo+','+json_result['CurrentPort']+'->'+json_result['RemotePort']
                    obj.save()
                    # 获取端口信息如果启用，打开端口
                    try:
                        NetThroughHearbeat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        NetThroughHearbeat.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                        NetThroughHearbeat.connect(("127.0.0.1", 9000))
                        JsonStr = {'IsOne': False, 'EstablishPort': False, 'OpenPort': True,'ClosePort': False,
                                   'CurrentPort': json_result['CurrentPort']}
                        NetThroughHearbeat.send(bytes(json.dumps(JsonStr), encoding='utf-8'))
                        NetThroughHearbeat.close()
                    except Exception as e:
                        print(e)
                        NetThroughHearbeat.close()
                else:
                    return HttpResponse('no')
        return HttpResponse(json.dumps({
            "status": 'status',
            "result": 'result'
        }))

def DelUser(request):
    if (request.method == 'POST'):
        PostBody = request.body.decode('UTF-8')
        json_result = json.loads(PostBody)
        userid=json_result['id']
        obj = models.RuiNetworkUser.objects.get(id=userid)
        models.RuiNetworkUser.objects.filter(id=userid).delete()
        models.RuiNetPorttable.objects.filter(UserID=obj.UserID).delete()
        return HttpResponse(json.dumps({
            "status": 'status',
            "result": 'result'
        }))

def DelPort(request):
    if (request.method == 'POST'):
        PostBody = request.body.decode('UTF-8')

        json_result = json.loads(PostBody)
        print(json_result)
        portid = json_result['id']
        models.RuiNetPorttable.objects.filter(id=portid).delete()
        return HttpResponse(json.dumps({
            "status": 'status',
            "result": 'result'
        }))
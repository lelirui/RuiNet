from django.db import models

# Create your models here.
class RuiNetPorttable(models.Model):
    #0为不在线
    id = models.AutoField('PortID',primary_key=True)
    CurrentPort=models.CharField('本地端口',max_length=5)
    RemotePort=models.CharField('远程端口',max_length=5)
    NetworkProtocol=models.CharField('网络协议',max_length=5)
    IsAlive = models.CharField('是否存活', max_length=1)
    PortFlow = models.CharField('端口流量', max_length=10)
    ProtStatus = models.CharField('端口状态', max_length=10)
    RemoteIP = models.CharField('远程IP', max_length=20)
    CurrentIP = models.CharField('本地IP', max_length=20)
    UserID = models.CharField('用户ID', max_length=20)
    PortEndTime=models.DateField('有效期')

class RuiNetworkUser(models.Model):
    id = models.AutoField('UserID', primary_key=True)
    UserID = models.CharField('用户ID', max_length=20)
    UserName = models.CharField('用户名称', max_length=20)
    UserOnlineStatus = models.CharField('用户在线状态', max_length=1)
    PortInfo = models.CharField('端口信息', max_length=50)
    UserKey = models.CharField('用户密钥', max_length=20)
    IsLimit = models.CharField('是否限制端口', max_length=1)
    PortLimitNum = models.CharField('限制端口数目', max_length=10)
    Email = models.CharField('Email', max_length=20)
    UserDisable = models.CharField('用户是否禁用', max_length=1)



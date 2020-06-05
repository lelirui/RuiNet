from django.urls import path,re_path
from RuiNetworkApp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
urlpatterns = [
    path('',views.index),
    re_path('^index',views.index),
    re_path('^tables',views.tables),
    re_path('^form-wizard',views.AddPort),
    re_path('^user-list',views.UserList),
    re_path('^new-user',views.NewUser),
    re_path('^moduser',views.ModUser),
    re_path('^modport',views.ModPort),
    re_path('^deluser',views.DelUser),
    re_path('^delport',views.DelPort),


]
urlpatterns += staticfiles_urlpatterns()
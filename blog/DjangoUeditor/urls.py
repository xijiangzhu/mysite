# coding:utf-8
from django import VERSION
from .widgets import UEditorWidget, AdminUEditorWidget
from .views import get_ueditor_controller
#from django.conf.urls import url
from django.urls import path,include,re_path #增加

urlpatterns = [
    re_path(r'^controller/$', get_ueditor_controller),
]

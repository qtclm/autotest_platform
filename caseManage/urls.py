from django.conf.urls import url
from django.urls import path,include,re_path
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    re_path(r'report/', views.report),
]
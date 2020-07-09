
from django.conf.urls import url,include
from django.contrib import admin

from backend import views
urlpatterns = [
    url(r'^server/', views.server),
    url(r'^asset/', views.asset),
    url(r'^idc/', views.idc),
    url(r'^ajax_server/', views.ajax_server),
    url(r'^ajax_asset/', views.ajax_asset),
    url(r'^get_config/', views.get_config),
    url(r'^modify/', views.modify),
    url(r'^get_product_line/', views.get_product_line),
    url(r'^get_idc/', views.get_idc),

]

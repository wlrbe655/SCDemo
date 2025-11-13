"""SCDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.views.static import serve
from django.conf import settings
from app01 import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.xcc_list,name='xcc_list'),
    path('xcc/list/',views.xcc_list),
    path('sc/list/', views.sc_list),
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT},name='media'),
    path('sc/add/',views.sc_add),
    path('sc/edit/',views.sc_edit),
    path('sc/delete/',views.sc_delete),
    path('login/',views.sc_login),
    path('register/',views.register),
    path('image/code/', views.image_code),
    path('user/list/', views.user_list),
    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/edit/', views.admin_edit),
    path('admin/delete/', views.admin_delete),
    path('cart/',views.cart),
    path('pay/',views.pay),
    path('checkout/',views.checkout),
    path('job/list/',views.job_list),
    path('order/list/', views.order_list),
    path('assign-delivery/<int:order_id>/', views.assign_delivery, name='assign_delivery'),
    path('job/add/',views.job_add),
    path('job/edit/',views.job_edit),
    path('job/delete/',views.job_delete),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path('123/123/',views.sc_order_update_status,name='sc_order_update_status')
    path('pay_is/', views.pay_is, name='pay_is'),
    path('assign-delivery/', views.assign_delivery, name='assign_delivery'),
    path('user/order/', views.user_order, name='user_order'),
    path('complete_order/<int:order_id>/', views.complete_order, name='complete_order'),
    path('logout/', views.user_logout, name='logout'),

]

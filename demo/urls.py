"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from basic.views import index,logon,login,password_recovery,logout,services,dentists,contact
from patient.views import info,register,search
from manager.views import service_manage,service_edit,service_delete,register_manage,register_edit,register_delete,patient_manage,patient_edit,patient_delete,dentist_manage, dentist_edit, dentist_delete,contact_manage
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('logon/',logon),
    path('login/',login),
    path('password_recovery/',password_recovery),
    path('logout/',logout),
    url(r'^captcha',include('captcha.urls')),
    path('info/',info),
    path('services/',services),
    path('register/',register),
    path('search/',search),
    path('dentists/',dentists),
    path('contact/',contact),
    path('service_manage/',service_manage),
    path('service_edit/<int:service_id>/', service_edit, name='service_edit'),
    path('service_delete/<int:service_id>/', service_delete, name='service_delete'),
    path('register_manage/',register_manage),
    path('register_edit/<int:register_id>/',register_edit,name='register_edit'),
    path('register_delete/<int:register_id>/',register_delete,name='register_delete'),
    path('patient_manage/',patient_manage),
    path('patient_edit/<int:patient_id>/',patient_edit,name='patient_edit'),
    path('patient_delete/<int:patient_id>/',patient_delete,name='patient_delete'),
    path('dentist_manage/',dentist_manage),
    path('dentist_edit/<int:dentist_id>/', dentist_edit, name='dentist_edit'),
    path('dentist_delete/<int:dentist_id>/', dentist_delete, name='dentist_delete'),
    path('contact_manage/',contact_manage)
]

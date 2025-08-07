from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('userreg/',views.userreg,name='userreg'),
    path('insertuser/',views.insertuser,name='insertuser'),
    path('login/',views.login,name='login'),
    path('login_check/',views.login_check,name='login_check'),
    path('adlogin/', views.adlogin, name='adlogin'),
    path('adlogin_check',views.adlogin_check,name='adlogin_check'),
    path('deleteprofile/<int:id>',views.deleteprofile,name='deleteprofile'),
    path('editprofile/<int:id>/',views.view,name='viewprofile'),
    path('viewprofile/<int:id>',views.view,name='viewprofile'),
    path('otp/',views.otp_verify,name="otp_verify"),
    path('verify_otp/', views.otp_verify, name='verify_otp'),
    path('viewusers/',views.viewusers,name='viewusers'),
    path('ranking/',views.ranking,name='ranking'),
    path('viewusers/', views.adlogin_check, name='viewusers'),
    path('c_fill/<int:id>/', views.c_fill, name='c_fill'),
    path('save_choices/',views.save_choices,name='save_choices'),
    path('allot/',views.allot,name='allot'),
] 



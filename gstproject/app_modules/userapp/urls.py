from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app_modules.userapp import views


app_name = 'userapp'

urlpatterns = [
    path('',views.UserIndexView.as_view(),name="userindex"),
    path('userforgotpassword/',views.UserForgotPasswordView.as_view(),name="userforgotpassword"),
    path('userresetpassword/',views.UserResetPassword.as_view(),name="userresetpassword"),
    path('userlogin/',views.UserLoginView.as_view(),name="userlogin"),
    path('userregister/',views.UserRegisterView.as_view(),name="userregister"),
    path('userlogout/',views.UserLogoutView.as_view(),name="userlogout"),
    path('userchat/',views.UserChatView.as_view(),name="userchat"),
]
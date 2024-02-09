from django.urls import path
from account import views

urlpatterns = [
    path('', views.view_login , name="login_view"),
    path('account/reigster_view', views.register_view, name="register_view"),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<str:uidb64>/<str:token>/', views.account_activate, name='activate'),
    path('account/second_register_view', views.second_register_view,name="second_register_view"),
    path('account/home', views.home,name="home"),
    path('account/analitycs', views.analitycs,name="analitycs"),
    path('account/logout', views.logout_view,name="logout_view")
]

from django.urls import path
from account import views

urlpatterns = [
    path('', views.view_login , name="login_view"),
    path('account/reigster_view', views.register_view, name="register_view"),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<str:uidb64>/<str:token>/', views.account_activate, name='activate'),
    path('account/second_register_view', views.second_register_view,name="second_register_view"),
    path('account/change_password',views.change_password,name='change_password'),
    path('account/show_reset_password', views.show_reset_password, name='show_reset_password'),
    path('account/reset_password/', views.reset_password, name='reset_password'),
    path('account/reset_password_confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('account/home', views.home,name="home"),
    path('account/logout', views.logout_view,name="logout_view"),
    path('account/show_all_expense',views.show_all_expense,name="show_all_exp")
]

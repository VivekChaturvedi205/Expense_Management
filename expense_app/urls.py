from django.urls import path
from expense_app import views

urlpatterns = [
    path('add_expense',views.expense_details,name="expense_details"),
    path('del_expense/<int:id>/',views.del_expense,name="delete_expense"),
    path('update_expense/<int:id>/',views.update_expense,name="update_expense"),
    path('visualize-expenses/', views.visualize_expenses, name='visualize_expenses'),
]

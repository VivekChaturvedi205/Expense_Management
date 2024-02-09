from django.contrib import admin
from .models import Reimbursement,Budget,MonthWiseExpense

@admin.register(Reimbursement)
class ReimbursementAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'description', 'is_approved')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'budget')
    

@admin.register(MonthWiseExpense)
class MonthWiseExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'month')

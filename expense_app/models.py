from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Reimbursement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_approved = models.BooleanField(default=False)
    image_data=models.TextField(blank=True, null=True)
    expense_date = models.DateField()
    expense_name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255,null=True,blank=True)
    file_extension = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(null=True,blank=True)
    delete_at = models.DateField(null=True,blank=True)

    def __str__(self):
        return f"Reimbursement for {self.user.username} - {self.amount}"
    
class Budget(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, unique=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Budget for {self.user.username} - {self.budget}"


class MonthWiseExpense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    month = models.CharField(max_length=20)
    year = models.IntegerField(null=True, blank=True) 
    total_expense = models.IntegerField()
    remain_expense = models.IntegerField()
    calculation_date = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_payment_done = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'month','year']

    def __str__(self):
        return f"{self.user.username}'s expenses for {self.month}"
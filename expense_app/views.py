from django.shortcuts import get_object_or_404, render, redirect
from .models import MonthWiseExpense, Reimbursement
import base64
from django.utils import timezone
from account.models import CustomUser
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from .models import Budget

def expense_details(request):
    if request.method == 'POST':
        user_id = request.user.id
        amount = request.POST.get('amount')
        expense_name = request.POST.get('expense_name')
        description = request.POST.get('description')
        date1 = request.POST.get('date')

        try:
            file = request.FILES['file']
            file_name, file_extension = str(file.name).split('.')[0], str(file.name).split('.')[1]
            file_content = file.read()
            encoded_file = base64.b64encode(file_content).decode('utf-8')
        except KeyError:
            encoded_file = None

        expense = Reimbursement.objects.create(
            user_id=user_id,
            amount=amount,
            expense_name=expense_name,
            description=description,
            expense_date=date1,
            image_data=encoded_file,
            file_name=file_name,
            file_extension=file_extension
        )
        return redirect('home')

    return render(request, 'expense.html')


def del_expense(request, id):
    reimbursement = get_object_or_404(Reimbursement, pk=id)
    reimbursement.delete()
    return redirect('home')

def update_expense(request, id):
    reimbursement = get_object_or_404(Reimbursement, pk=id)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        expense_name = request.POST.get('expense_name')
        description = request.POST.get('description')
        date1 = request.POST.get('date')

        try:
            file = request.FILES['file']
            file_name, file_extension = str(file.name).split('.')[0], str(file.name).split('.')[1]
            file_content = file.read()
            encoded_file = base64.b64encode(file_content).decode('utf-8')
        except KeyError:
            encoded_file = None
        reimbursement.amount = amount
        reimbursement.expense_name = expense_name
        reimbursement.description = description
        reimbursement.expense_date = date1
        if encoded_file is not None:
            reimbursement.image_data = encoded_file
            reimbursement.file_name = file_name
            reimbursement.file_extension = file_extension
        reimbursement.save()

        return redirect('home')

    return render(request, 'update_expense.html', {'reimbursement': reimbursement})

def running(user):
    current_user = CustomUser.objects.get(username=user)
    current_datetime = timezone.now()
    print(current_datetime.day)
    str_current_year = current_datetime.year
    str_current_month = current_datetime.month
    if current_datetime.day == 1 and current_datetime.hour < 12:
        previous_datetime = current_datetime - timezone.timedelta(days=1)
        str_previous_year = previous_datetime.year
        str_previous_month = previous_datetime.month
        perform_calculation(current_user, str_previous_year, str_previous_month)
    perform_calculation(current_user, str_current_year, str_current_month)

def perform_calculation(current_user, str_year, str_month):
    budget = Budget.objects.filter(user_id=current_user.id).values('budget').first()
    budget = budget['budget'] if budget else 0
    total_amount = Reimbursement.objects.filter(
        user_id=current_user.id,
        delete_at__isnull=True,
        expense_date__month=str_month,
        expense_date__year=str_year
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    try:
        user_month_wise_expense = MonthWiseExpense.objects.get(
            user_id=current_user.id,
            month=str_month,
            year=str_year
        )
        user_month_wise_expense.total_expense += total_amount
        user_month_wise_expense.remain_expense = budget - user_month_wise_expense.total_expense
        user_month_wise_expense.calculation_date = timezone.now()
        user_month_wise_expense.save()
    except MonthWiseExpense.DoesNotExist:
        user_month_wise_expense = MonthWiseExpense.objects.create(
            user_id=current_user.id,
            month=str_month,
            year=str_year,
            total_expense=total_amount,
            remain_expense=budget - total_amount,
            calculation_date=timezone.now()
        )
    return None


def visualize_expenses(request):
    admincount=CustomUser.objects.filter(user_type='admin').count()
    managercount=CustomUser.objects.filter(user_type='manager').count()
    candidatecount=CustomUser.objects.filter(user_type='candidate').count()
    submit_expense = Reimbursement.objects.all().count()
    pending_expense = Reimbursement.objects.filter(is_approved=False, delete_at__isnull=True).count()
    approve_expense = Reimbursement.objects.filter(is_approved=True).count()
    rejected_expense = Reimbursement.objects.filter(is_approved=False, delete_at__isnull=False).count()
    total_budget = Budget.objects.aggregate(total_amount=Sum('budget'))
    total_approve_budget = Reimbursement.objects.filter(is_approved=True).aggregate(total_amount=Sum('amount'))
    total_budget_amount = int(total_budget['total_amount']) if total_budget['total_amount'] is not None else 0.0
    total_approve_budget_amount = int(total_approve_budget['total_amount']) if total_approve_budget['total_amount'] is not None else 0.0    
    context = {
        'admincount': admincount,
        'managercount': managercount,
        'candidatecount':candidatecount,
        'submit_expense':submit_expense,
        'pending_expense':pending_expense,
        'approve_expense':approve_expense,
        'rejected_expense':rejected_expense,
        'total_budget_amount':total_budget_amount,
        'total_approve_budget_amount':total_approve_budget_amount
    }
    return render(request, 'visualize_expenses.html', context)
from django.shortcuts import get_object_or_404, render, redirect
from .models import Reimbursement
import base64

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



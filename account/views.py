from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.genertor_password import generated_password
from django.contrib.auth.decorators import login_required
from expense_app.models import Budget
from expense_app.models import Reimbursement
from account.models import CustomUser
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from expense_app.views import *

# Activation mail
def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

# Main Register
def register_view(request):
    if request.method == 'POST':
        password = request.POST.get('psw')
        confirm_password = request.POST.get('psw1')
        email = request.POST.get('email')
        if password == confirm_password:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, f'The email "{email}" is already registered. Please log in.', extra_tags='email_exists')
                return redirect('login_view')
            user = CustomUser.objects.create_user(username=email,email=email, password=password,user_type="admin")
            user.is_verified=False
            user.save()
            current_site = get_current_site(request)
            protocol = 'http'  
            activation_url = f'{protocol}://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/'
            subject = 'Activate Your Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'protocol': protocol,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            email = EmailMessage(subject, message, 'your_email@example.com', [user.email])
            email.content_subtype = 'html'
            email.send()
            return redirect('account_activation_sent')
        else:
            messages.error(request, 'Passwords do not match.', extra_tags='password_mismatch')
    return render(request, 'signup.html')

# Account Verified
def account_activate(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        return redirect('login_view')
    else:
        return render(request, 'account_activation_invalid.html')

# Main Login
def view_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('psw')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid login credentials. Please sign up.')
            return redirect('signup')

        try:
            authenticated_user = authenticate(request, username=email, password=password)
            if authenticated_user is not None and authenticated_user.is_verified:
                login(request, authenticated_user)
                messages.success(request, f"Welcome, {authenticated_user.email}! You have successfully logged in.")
                return redirect('home')
            else:
                print(f"Authentication failed for user: {email}")
                messages.error(request, 'Invalid login credentials or email not verified user.')
        except ValueError as e:
            print(f"Error during login: {e}")
    return render(request, 'login.html')

# Analytics Page
@login_required(login_url='login_view')  
def logout_view(request):
    auth_logout(request)
    return redirect('login_view')

# logout page
# @login_required(login_url='login_view')  
# def analitycs(request):
#     return render(request, 'analitycs.html')

# Admin and Manager page for create candidate
@login_required(login_url='login_view')  
def second_register_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        budget_amount = request.POST.get('Budget')
        password = generated_password()
        email = request.POST.get('email')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, f'The email "{email}" is already registered. Please log in.', extra_tags='email_exists')
            return redirect('second_register_view')

        user = CustomUser.objects.create_user(username=email, email=email, password=password, user_type=user_type, is_verified=True)
        budget = Budget.objects.create(user=user, budget=budget_amount)
        current_site = get_current_site(request)
        protocol = 'http'  
        subject = 'Account Details'
        message = render_to_string('share_email_password.html', {
                'user': user,
                'domain': current_site.domain,
                'protocol': protocol,
                'password': password
            })

        email = EmailMessage(subject, message, 'your_email@example.com', [user.email])
        email.content_subtype = 'html'
        email.send()
        return redirect('home')
    else:
        messages.error(request, 'Invalid request method.', extra_tags='invalid_request_method')

    return render(request, 'second_signup.html')

def show_reset_password(request):
    return render(request, 'reset_password.html')

# Reset Password
def reset_password(request):
    try:
        if request.method == 'POST':
            username=request.POST.get('username')
            user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('login_view')
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[uidb64, token]))
    subject = 'Password Reset Request'
    message = f'Click the following link to reset your password:\n\n{reset_link}'
    message = render_to_string('reset_password_link.html', {
            'user': user,
            'reset_link': reset_link,
        })

    email = EmailMessage(subject, message, 'your_email@example.com', [user.email])
    email.content_subtype = 'html'
    email.send()
    messages.success(request, 'Password reset link sent to your email.')
    return redirect('login_view')  

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('login_view')
            else:
                messages.error(request, 'Passwords do not match. Please try again.')

        return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'Invalid password reset link.')
        return redirect('login_view')
    

@login_required(login_url='login_view')  
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('psw')
        confirm_password = request.POST.get('psw1')
        if new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')
    return render(request, 'change_password.html')

# Home Page
@login_required(login_url='login_view')
def home(request):
    if request.user.user_type == 'admin':
        pass
    else:
        running(request.user.username)
    if request.user.user_type == 'admin' or request.user.user_type == 'manager':
        print('if')
        reimbursement = Reimbursement.objects.filter(Q(delete_at__isnull=True) & Q(is_approved=False)).order_by('-created_at', '-update_at')
    else:
        print('else')
        reimbursement = Reimbursement.objects.filter(user=request.user.id, delete_at__isnull=True,is_approved=False).order_by('-created_at', '-update_at').all()
    return render(request, 'home.html', {'reimbursement': reimbursement})

@login_required(login_url='login_view')
def show_all_expense(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        selected_expense_ids = request.POST.getlist('selected_expenses')
        print(action,selected_expense_ids)
        if action == 'approve':
            Reimbursement.objects.filter(id__in=selected_expense_ids).update(is_approved=True)
            messages.success(request, f'Successfully approved {len(selected_expense_ids)} expenses.')
        elif action == 'reject':
            Reimbursement.objects.filter(id__in=selected_expense_ids).update(is_approved=False,delete_at=timezone.now())
            messages.success(request, f'Successfully rejected {len(selected_expense_ids)} expenses.')
        return redirect('show_all_exp')
    if request.user.user_type == 'admin' or request.user.user_type == 'manager':
        reimbursement = Reimbursement.objects.filter(Q(delete_at__isnull=True) & Q(is_approved=False)).order_by('-created_at', '-update_at')
    else:
        reimbursement = Reimbursement.objects.filter(user=request.user.id, delete_at__isnull=True, is_approved=False).order_by('-created_at', '-update_at')
    items_per_page = 1
    paginator = Paginator(reimbursement, items_per_page)
    page = request.GET.get('page')
    try:
        reimbursement = paginator.page(page)
    except PageNotAnInteger:
        reimbursement = paginator.page(1)
    except EmptyPage:
        reimbursement = paginator.page(paginator.num_pages)
    return render(request, 'show_all_expense.html', {'reimbursement': reimbursement})

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
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


# Home Page
@login_required(login_url='login_view')  
def home(request):
    if request.user.user_type == 'admin' or request.user.user_type == 'manager':
        reimbursement=Reimbursement.objects.all()
    else:
        reimbursement=Reimbursement.objects.filter(user=request.user.id)
    return render(request, 'home.html',{'reimbursement':reimbursement})

# Analytics Page
@login_required(login_url='login_view')  
def logout_view(request):
    auth_logout(request)
    return redirect('login_view')

# logout page
@login_required(login_url='login_view')  
def analitycs(request):
    return render(request, 'analitycs.html')

# Admin and Manager page for create candidate
def second_register_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        budget_amount = request.POST.get('Budget')
        password = generated_password()
        email = request.POST.get('email')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, f'The email "{email}" is already registered. Please log in.', extra_tags='email_exists')
            return redirect('second_register_view')

        user = CustomUser.objects.create_user(username=email, email=email, password=password, user_type=user_type)
        budget = Budget.objects.create(user=user, budget=budget_amount)
        return redirect('home')
    else:
        messages.error(request, 'Invalid request method.', extra_tags='invalid_request_method')

    return render(request, 'second_signup.html')


# Reset Password
def reset_password(request):
    pass

def change_password(request):
    pass








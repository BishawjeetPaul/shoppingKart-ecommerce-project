from django.shortcuts import render, redirect
from account.models import Account
from django.contrib import messages, auth
from django.contrib.auth import login, logout
from .EmailBackEnd import EmailBackEnd

# this function for user registration or user verification via email address.
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = email.split("@")[0]
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        print(password)
        print(password_confirm)

        if (password == password_confirm):
            try:
                user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password,
                    phone_number=phone_number
                )
                user.save()
                messages.success(request, "Thank you for registering with us.")
                return redirect("register")
            except:
                messages.error(request, "Registration failed..!")
                return redirect("register")
        else:
            messages.error(request, "Password does not match..!")
    return render(request, 'register.html')

# this function for user login to send OTP in user email address
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request, username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect('login')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You are logged out.")
    return redirect('login')


def dashboard(request):
    return render(request, 'includes/main-dashboard.html')
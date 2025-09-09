from django.shortcuts import render, redirect
from account.models import Account
from django.contrib import messages, auth
from .EmailBackEnd import EmailBackEnd
# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage




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

                # USER ACTIVATION
                current_site = get_current_site(request) # get the current site
                mail_subject = 'Please activate your account'
                # send verification message details in user email address
                message = render_to_string('account/account_verification_mail.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })

                # send email to the user
                to_mail = email
                send_email = EmailMessage(mail_subject, message, to=[to_mail])
                send_email.send()

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

# this function for user logout.
def logout_user(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('login')

# this function for admin panel
def dashboard(request):
    return render(request, 'includes/main-dashboard.html')
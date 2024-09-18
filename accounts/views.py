from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import User
from .utils import send_verification_mail
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        match1 = User.objects.filter(username=username).exists()
        match2 = User.objects.filter(email=email).exists()
        if match1 and match2:
            messages.error(request, "Use different username and email")
        elif match1:
            messages.error(request, "Use different username")
        elif match2:
            messages.error(request, "Use different email") 
        else:
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            pward = request.POST.get('password')
            cpward = request.POST.get('confirm_password')
            role=request.POST.get('role')
            if pward == cpward:
                user=User.objects.create(username=username,
                                         first_name=fname,
                                         last_name=lname,
                                         email=email,role=role)
                user.set_password(pward)
                user.save()
                # To send verification mail
                send_verification_mail(request, user)
                messages.success(request, "Account is created")
                return redirect('login')
            else:
                messages.error(request, "Password & Confirm Password not Matched")
    return render(request,'accounts/register.html')

# For email verification and activating email
def activate(request, uidb64, token):
    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user= User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user= None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active= True
        user.save()
        messages.success(request, "Congratulations! Your account has been activated")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('login')

def login(request):
    if request.method=='POST':
        email= request.POST['email']
        password= request.POST['password']
        user= auth.authenticate(email=email,password= password)
        if user is not None:
            auth.login(request, user)
            if user.role==1:
                return redirect('opsUserDashboard')
            elif user.role==2:
                return redirect('clientUserDashboard')
            else:
                return redirect('admin/')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'accounts/login.html')

@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url= 'login')
def clientUserDashboard(request):
    return redirect('downloadFile')

@login_required(login_url= 'login')
def opsUserDashboard(request):
    return redirect('uploadFile')

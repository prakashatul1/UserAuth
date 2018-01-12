from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.contrib.auth import authenticate
from accounts.forms import RegistrationForm,EditProfileForm,EditUserProfileForm, ResetPasswordForm, SetPasswordForm
from .models import User,UserProfile
from django.core.mail import send_mail
import hashlib

@login_required
def view_all(request):
    user = authenticate(email=request.user.email, password=request.user.password)
    if user is not None:
        login(request, user)
    user_list = UserProfile.objects.filter(is_live=True)
    table = {'user_list': user_list}
    update_session_auth_hash(request, user)
    return render(request,'accounts/view_all.html',table)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account/login')
    else:
        form = RegistrationForm()
        args = {"form":form}
        return render(request,'accounts/reg_form.html',args)

@login_required
def view_profile(request):
    args = {'user':request.user}
    return render(request,'accounts/profile.html',args)

@login_required
def edit_profile(request):
    userprofile = UserProfile.objects.get(user=request.user)
    initial = {'description':userprofile.description,'city':userprofile.city,'website':userprofile.website,'phone':userprofile.phone}
    if request.method=='POST':
        form1 = EditProfileForm(request.POST, instance=request.user)
        form2 = EditUserProfileForm(request.POST, instance=request.user)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('/account/profile')
    else:
        form1 = EditProfileForm(instance=request.user)
        form2 = EditUserProfileForm(initial=initial,instance=request.user)
        args = {
                    'form1':form1,
                    'form2':form2,
                }
        return render(request,'accounts/edit_profile.html',args)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('/account/profile')
        else:
            return redirect('account/change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

@login_required
def delete_profile(request):
    userprofile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        userprofile.is_live = False
        userprofile.save()
        return redirect('/account/profile/view_all')
    else:
        return render(request,'accounts/delete_profile.html',{'user':userprofile})

def password_reset(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            if form.data['email'] in (User.objects.values_list('email',flat=True)):
                user = User.objects.get(email=form.data['email'])
                token = hashlib.md5(str(user.id)).hexdigest()
                user.userprofile.token = token
                user.userprofile.save()
                reset_password_link = 'http://127.0.0.1:8000/account/password_reset/confirm/?token='+str(token)+'&id='+str(user.id)
                email_body = 'Hi, you can click the following link to reset your password\n\n'+reset_password_link
                send_mail(
                    'Reset Password',
                    email_body,
                    'atul.prakash@stayabode.com',
                    [form.data['email'],],
                    fail_silently=False,
                )
                return redirect('/account/reset_password/done/')
            return HttpResponse('This email id does not exist')
        else:
            return HttpResponse('Enter a valid email id')
    else:
        form = ResetPasswordForm()
        args = {'form':form}
        return render(request,'accounts/password_reset.html',args)

def password_reset_confirm(request):
    # import ipdb;ipdb.set_trace()
    token = request.GET.get('token')
    id = request.GET.get('id')
    user = User.objects.get(pk=id)
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.data['password'])
            user.save()
            return HttpResponse('You password was reset successfully.<br><br>You can login <a href="http://127.0.0.1:8000/">here</a> ')
    else:
        if user.userprofile.token == token:
            form = SetPasswordForm()
            args = {'form':form}
            return render(request,'accounts/password_reset_confirm.html',args)
        else:
            return HttpResponse('Token expired')

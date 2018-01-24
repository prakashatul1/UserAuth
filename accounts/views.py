import hashlib
from ast import literal_eval
# import requests
# from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm,AuthenticationForm
from django.contrib.auth import update_session_auth_hash,login,logout
from django.contrib.auth.decorators import login_required
from accounts.forms import RegistrationForm,EditProfileForm,EditUserProfileForm, ResetPasswordForm, SetPasswordForm, SendEmailForm
from django.core.mail import send_mail
from .models import User,UserProfile
from django.http import JsonResponse
from html2text import html2text



# class UserProfileList(generics.ListCreateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#
#     def perform_create(self, serializer):
#         serializer.save()
#
# class DetailsView(generics.RetrieveUpdateDestroyAPIView):
#
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer

class UserProfileList(APIView):

    def get(self,request):
        result = []
        for each in User.objects.all():
            result.append(each.userprofile.as_json())
        return JsonResponse(result,safe=False)

    def post(self,request):
        data_dict = literal_eval(request.body)
        print data_dict
        try:
            user = User.objects.create(
                username=data_dict.get('username'),
                email = data_dict.get('email'),
                first_name = data_dict.get('first_name'),
                last_name = data_dict.get('last_name'),
                password = data_dict.get('password'),
            )
        except:
            return JsonResponse({'msg': 'Invalid data'})
        try:
            user.userprofile.phone = data_dict.get('phone')
            user.userprofile.website = data_dict.get('website')
            user.userprofile.city = data_dict.get('city')
            user.userprofile.description = data_dict.get('description')
            user.userprofile.save()
        except:
            return JsonResponse({'msg1': 'User created succesfully','msg2': 'Userprofile created succesfully withe empty data', 'userid': user.id})

        return JsonResponse({'msg':'User created succesfully','userid':user.id})


class DetailsView(APIView):

    def get(self,request,pk):
        result =[]
        try:
            user = User.objects.get(pk=pk)
        except:
            return JsonResponse({"msg": "User not found"})
        result.append(user.userprofile.as_json())
        return JsonResponse(result, safe=False)

    def put(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except:
            return JsonResponse({"msg": "User not found"})
        pass
        data_dict = literal_eval(request.body)
        edited = False
        if 'email' in data_dict.keys():
            user.email = data_dict['email']
            edited = True
        if 'first_name' in data_dict.keys():
            user.email = data_dict['first_name']
            edited = True
        if 'last_name' in data_dict.keys():
            user.email = data_dict['last_name']
            edited = True
        if 'phone' in data_dict.keys():
            user.userprofile.phone = data_dict['phone']
            edited = True
        if 'website' in data_dict.keys():
            user.userprofile.website = data_dict['website']
            edited = True
        if 'city' in data_dict.keys():
            user.userprofile.city = data_dict['city']
            edited = True
        if 'description' in data_dict.keys():
            user.userprofile.description = data_dict['description']
            edited = True
        if edited == True:
            user.save()
            user.userprofile.save()
            return JsonResponse({"msg": "User successfully modified"})
        return JsonResponse({"msg":"Invalid data"})


    def delete(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except:
            return JsonResponse({"msg": "User not found"})
        user.delete()
        return JsonResponse({"msg":"User has been deleted"})


# @csrf_exempt
# def userprofileapiview(request):
#     result = []
#
#     if request.method == 'POST':
#         data_dict = literal_eval(request.body)
#         try:
#             user = User.objects.create(
#                 username=data_dict.get('username'),
#                 email = data_dict.get('email'),
#                 first_name = data_dict.get('first_name'),
#                 last_name = data_dict.get('last_name'),
#                 password = data_dict.get('password'),
#             )
#         except:
#             return JsonResponse({'msg': 'Invalid data'})
#         try:
#             user.userprofile.phone = data_dict.get('phone')
#             user.userprofile.website = data_dict.get('website')
#             user.userprofile.city = data_dict.get('city')
#             user.userprofile.description = data_dict.get('description')
#             user.userprofile.save()
#         except:
#             return JsonResponse({'msg1': 'User created succesfully','msg2': 'Userprofile created succesfully withe empty data', 'userid': user.id})
#
#         return JsonResponse({'msg':'User created succesfully','userid':user.id})
#
#     if request.method == 'GET':
#         for each in User.objects.all():
#             result.append(each.userprofile.as_json())
#
#         return JsonResponse(result,safe=False)
#
# @csrf_exempt
# def userdetailapiview(request,pk):
#     result = []
#     if request.method == 'GET':
#         try:
#             user = User.objects.get(pk=pk)
#         except:
#             return JsonResponse({"msg": "User not found"})
#         result.append(user.userprofile.as_json())
#         return JsonResponse(result, safe=False)
#
#     if request.method == 'DELETE':
#         try:
#             user = User.objects.get(pk=pk)
#         except:
#             return JsonResponse({"msg": "User not found"})
#         user.delete()
#         return JsonResponse({"msg":"User has been deleted"})
#
#     if request.method == 'PUT':
#         try:
#             user = User.objects.get(pk=pk)
#         except:
#             return JsonResponse({"msg": "User not found"})
#         pass
#         data_dict = literal_eval(request.body)
#         edited = False
#         if 'email' in data_dict.keys():
#             user.email = data_dict['email']
#             edited = True
#         if 'first_name' in data_dict.keys():
#             user.email = data_dict['first_name']
#             edited = True
#         if 'last_name' in data_dict.keys():
#             user.email = data_dict['last_name']
#             edited = True
#         if 'phone' in data_dict.keys():
#             user.userprofile.phone = data_dict['phone']
#             edited = True
#         if 'website' in data_dict.keys():
#             user.userprofile.website = data_dict['website']
#             edited = True
#         if 'city' in data_dict.keys():
#             user.userprofile.city = data_dict['city']
#             edited = True
#         if 'description' in data_dict.keys():
#             user.userprofile.description = data_dict['description']
#             edited = True
#         if edited == True:
#             user.save()
#             user.userprofile.save()
#             return JsonResponse({"msg": "User successfully modified"})
#         return JsonResponse({"msg":"Invalid data"})



def loginview(request):
    if request.POST:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('/account/profile')
    form = AuthenticationForm()
    args = {"form": form}
    return render(request, 'accounts/login.html', args)

@login_required
def logoutview(request):
    logout(request)
    return render(request, 'accounts/logout.html')

@login_required
def view_all(request):
    user_list = UserProfile.objects.filter(is_live=True)
    table = {'user_list': user_list}
    return render(request,'accounts/view_all.html',table)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account/login')
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
    if request.method=='POST':
        userform = EditProfileForm(request.POST, instance=request.user)
        userprofileform = EditUserProfileForm(request.POST, instance=request.user.userprofile)
        if userform.is_valid() and userprofileform.is_valid():
            userform.save()
            userprofileform.save()
            return redirect('/account/profile')
    initial = {'description': userprofile.description, 'city': userprofile.city, 'website': userprofile.website,
               'phone': userprofile.phone}
    userform = EditProfileForm(instance=request.user)
    userprofileform = EditUserProfileForm(initial=initial)
    args = {
                'userform':userform,
                'userprofileform':userprofileform,
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
        return redirect('account/change_password')
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
        return HttpResponse('Enter a valid email id')
    form = ResetPasswordForm()
    args = {'form':form}
    return render(request,'accounts/password_reset.html',args)


def password_reset_confirm(request):
    token = request.GET.get('token')
    id = request.GET.get('id')
    user = User.objects.get(pk=id)
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.data['password'])
            user.save()
            return HttpResponse('You password was reset successfully.<br><br>You can login <a href="http://127.0.0.1:8000/">here</a> ')
    if user.userprofile.token == token:
        form = SetPasswordForm()
        args = {'form':form}
        return render(request,'accounts/password_reset_confirm.html',args)
    return HttpResponse('Token expired')

def send_email(request):
    if request.method == "POST":
        form = SendEmailForm(request.POST)
        try:
            for each in User.objects.filter(id__in=form.data.getlist('user')):
                body = form.data.get('body').replace('{{user}}', each.username)
                send_mail(
                    subject=form.data.get('subject'),
                    message=html2text(body),
                    from_email='atul.prakash@stayabode.com',
                    # recipient_list=User.objects.filter(id__in=form.data.getlist('user')).values_list('email', flat=True),
                    recipient_list=[each.email],
                    fail_silently=False,
                    html_message=body,
                    )
            return HttpResponse('email sent succesfully')
        except:
            return HttpResponse('Invalid data or email')
    form = SendEmailForm
    args = {'form': form}
    return render(request,'accounts/send_email.html',args)

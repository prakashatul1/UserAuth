from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # first_name = forms.CharField(required=True)
    # last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
        )

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'description',
            'city',
            'website',
            'phone',
        )

class ResetPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
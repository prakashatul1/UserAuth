from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import UserProfile
from ckeditor.widgets import CKEditorWidget

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

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


class SetPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)

class SendEmailForm(forms.Form):

    # userlist = User.objects.all()
    # choices = ()
    # for each in userlist:
    #     choices = choices + (each,)
    # user = forms.ChoiceField(widget=forms.Select,choices=choices)
    user = forms.ModelMultipleChoiceField(queryset = User.objects.all(),widget=forms.CheckboxSelectMultiple())
    subject = forms.CharField(max_length=20)
    body = forms.CharField(max_length=1000,widget=CKEditorWidget())

    class Meta:
        fields = ('user','subject','body')
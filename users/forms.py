from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
         model = User
         fields = ['email','first_name','last_name', 'password']

    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        instance = super(UserForm, self).save(commit=False)
        if commit:
            instance.username=email
            instance.set_password(password)
            instance.is_active=True
            instance.save()
        return instance



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','image')
            
class UserLogin(forms.Form):
    email=forms.CharField(max_length=150,widget=forms.EmailInput)
    password=forms.CharField(max_length=150,widget=forms.PasswordInput)

    def clean(self):
        user=authenticate(email=self.cleaned_data['email'],password=self.cleaned_data['password'])
        if not user:
            raise forms.ValidationError("Incorrect Username or Password")

    def sign_in(self):
        user=authenticate(email=self.cleaned_data['email'],password=self.cleaned_data['password'])
        return user

from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=64)
    password1 = forms.CharField(widget=forms.PasswordInput(), min_length=3)
    password2 = forms.CharField(widget=forms.PasswordInput(), min_length=3)


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=64)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=3)

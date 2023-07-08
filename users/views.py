from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, CreateView
from users.forms import RegisterForm, LoginForm


class RegisterCBV(CreateView):
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        context_data = {
            'form': RegisterForm
        }
        return render(request, self.template_name, context=context_data)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = RegisterForm(data=data)

        if form.is_valid():
            if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                user = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1')
                )
                return redirect('/users/login/')
            else:
                form.add_error('password1', 'Error! Passwords do not match!')
        return render(request, self.template_name, context={
            'form': form
        })


class LoginCBV(CreateView):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        context_data = {
            'form': LoginForm
        }
        return render(request, self.template_name, context=context_data)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = LoginForm(data=data)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                return redirect('/products')
            else:
                form.add_error('username', 'Password or Username is incorrect! Try again!')


class LogoutCBV(View):
    template_name = 'layouts/index.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/products/')



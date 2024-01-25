from django.shortcuts import render
from .models import Detection
from rest_framework_simplejwt.tokens import RefreshToken
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(View):
    def get(self, request):
        return render(request, 'myapp/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticar usuário
        user = authenticate(username=username, password=password)

        if user is not None:
            # Login bem-sucedido
            login(request, user)

            # Obter tokens de acesso e renovação
            refresh = RefreshToken.for_user(user)
            token_access = str(refresh.access_token)
            token_renewal = str(refresh)

            # Redirecionar para a página desejada com os tokens
            return render(request, 'success.html', {'token_access': token_access, 'token_renewal': token_renewal})
        else:
            # Credenciais inválidas
            return render(request, 'myapp/login.html', {'error': 'Credenciais inválidas'})

class LogoutView(View):
    def post(self, request):
        # Realizar logout
        logout(request)
        return render(request, 'myapp/logout.html')

class RenewView(View):
    def post(self, request):
        # Obter token de renovação
        token_renewal = request.POST.get('token_renewal')

        try:
            refresh_token = RefreshToken(token_renewal)
            token_access = str(refresh_token.access_token)
            return render(request, 'renew.html', {'token_access': token_access})
        except Exception as e:
            # Lidar com erros ao renovar o token
            return render(request, 'renew.html', {'error': str(e)})

def login_page(request):
    return render(request, "myapp/login.html")

class FirstPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'first_page.html')
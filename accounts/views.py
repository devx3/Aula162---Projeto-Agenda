from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


def index(request):
    return render(request, 'accounts/login.html')


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login feito com sucesso!')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')

    if not firstname or not lastname or not email or not username or not password or not password2:
        messages.error(request, 'Nenhum campo pode ser vazio')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except Exception:
        messages.error(request, 'Email inválido')
        return render(request, 'accounts/register.html')

    # password validation
    if password != password2:
        messages.error(request, 'As senhas são diferentes')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já existe')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Usuário já existe')
        return render(request, 'accounts/register.html')

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=firstname,
        last_name=lastname,
    )
    user.save()
    messages.success(request, 'Usuário registrado.')
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if form.is_valid():
        messages.success(request, f'Contato {request.POST.get("firstname")} adicionado')
        form.save()
        return redirect('dashboard')
    else:
        messages.success(request, 'Erro ao enviar formulário')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

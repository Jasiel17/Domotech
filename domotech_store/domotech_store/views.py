from django.contrib.messages.api import success
from django.http import HttpResponse
#responder mediante un template redrizado
from django.shortcuts import redirect, render  
from django.contrib.auth import authenticate
#encargada de generar sesion
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm

def index(request):
    #return HttpResponse('Hola mundo')
    return render(request,'index.html', {
        #contexto
        'message':'Lista de productos',
        'title': 'Productos',
        'products': [
            {'title':'Playera', 'price': 5, 'stock': True},
            {'title':'Camisa', 'price': 7, 'stock': True},
            {'title':'Vestido', 'price': 90, 'stock': False},
            {'title':'Bufanda', 'price': 78, 'stock': True},
        ]
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            #mensajes del servidor al cliente
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('index')
            # print("Usuario autenticado")
        else:
            messages.error(request, 'Usuario o contraseña no validos')
            print("usuario no autenticado")
    return render(request, 'users/login.html',{

    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada exitosamente')
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = RegisterForm(request.POST or None)
    #nos permite conocer si el form es valido
    if request.method == 'POST' and form.is_valid():
        # username=form.cleaned_data.get('username') 
        # email=form.cleaned_data.get('email')
        # password=form.cleaned_data.get('password')
        # print(username, email, password)
        # user = User.objects.create_user(username, email, password)
        user = form.save()
        if user:
            login(request,user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('index')
    return render(request, 'users/register.html',{
        #contexto, enviamos esto al html
        'form':form
    })
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Todo

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = Todo(user=request.user, todo_name=task)
        new_todo.save()
        messages.success(request, "Task added successfully!")
        return redirect('home-page')

    all_todo = Todo.objects.filter(user=request.user)
    context = {
        'all_todo': all_todo
    }
    return render(request, 'todoapp/todo.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'todoapp/register.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'todoapp/login.html')

@login_required(login_url='login')
def DeleteTask(request, name):
    get_todo = Todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('home-page')

@login_required(login_url='login')
def Update(request, name):
    get_todo = Todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')

def logoutpage(request):
    logout(request)
    return redirect('login')

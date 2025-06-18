from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import Todo
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from collections import defaultdict

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        emailid = request.POST.get('emailid')
        password = request.POST.get('password')
        print(username, emailid, password)
        my_user = User.objects.create_user(username, emailid, password)
        my_user.save()
        return redirect('/login')  

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/todo')
        else:
            return redirect('/login')

    return render(request, 'login.html')

@login_required(login_url='/login')
def todo_view(request):
    if request.method == 'POST':
        task_name=request.POST.get('task_name')
        description = request.POST.get('description', '')
        category=request.POST.get('category','personal')
        due_date = request.POST.get('due_date')
        obj = models.Todo(
            task_name=task_name,
            description=description,
            category=category,
            due_date=due_date,
            user=request.user
        )

        obj.save()
        tasks=models.Todo.objects.filter(user=request.user).order_by('due_date')
        return redirect('/todo',{'tasks':tasks})
    tasks=models.Todo.objects.filter(user=request.user).order_by('due_date')
    category_groups = defaultdict(list)
    for task in tasks:
        category_groups[task.category].append(task)

    return render(request, 'todo.html', {'tasks': tasks, 'category_groups': dict(category_groups)})
    return render(request, 'todo.html', {'tasks':tasks})


@login_required(login_url='/login')
def edit_view(request, sno):
    task = models.Todo.objects.get(sno=sno)
    if request.method == 'POST':
        task.task_name = request.POST.get('task_name')
        task.description = request.POST.get('description', '')
        task.category = request.POST.get('category', 'personal')
        task.save()
        return redirect('todo')  
    return render(request, 'edit_todo.html', {'task': task})

@login_required(login_url='/login')
def delete_view(request,sno):
    task = models.Todo.objects.get(sno=sno)
    task.delete()
    return redirect('todo')

def signout_view(request):
    logout(request)
    return redirect('/login')
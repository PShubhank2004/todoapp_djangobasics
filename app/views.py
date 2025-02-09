from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
# Create your views here.
def signup(request):
    if request.method =='POST':
        #username = request.POST.get('name')
        username = request.POST['name']
        emailid = request.POST['email']
        password= request.POST['password']
        confirmpassword= request.POST['confirm-password']
        
        myuser = User.objects.create_user(username,emailid,password)

        myuser.save()

        messages.success(request, "your account has been successfully created.")
        return redirect('login')
    return render(request,'signup.html')

def login_view(request):
    if request.method =='POST':
        username = request.POST['name']
        password= request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            name = user.username
            return redirect('main')
        else:
            messages.error(request,"bad credentials")
            return redirect('login')
    return render(request,'login.html')

def loggingout(request):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect('login')



@login_required
def main(request):
    if request.method == 'POST':
        res = Task.objects.filter(user=request.user).order_by('-date')
        title = request.POST.get('title')  # Get title from form input
        if title:  # Ensure the title is not empty
            Task.objects.create(title=title, user=request.user)
            
        return redirect('main')  # Redirect to the main page after adding a task
    
    # Fetch tasks for the logged-in user
    res = Task.objects.filter(user=request.user).order_by('-date')
    return render(request, 'main.html', {'res': res})



@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)  # Ensure only the task owner can delete
    task.delete()
    return redirect('main')



def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)  # Ensure only the task owner can edit
    
    if request.method == 'POST':
        title = request.POST.get('title')  # Get the updated title from form input
        if title:  # Ensure the title is not empty
            task.title = title
            task.save()  # Save changes to the task
            messages.success(request, "Task updated successfully.")
            return redirect('main')  # Redirect to the main page after editing
    
    return render(request, 'edit-task.html', {'task': task})  
    
            

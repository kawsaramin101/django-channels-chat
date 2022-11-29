from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import SignUpForm


CustomUser = get_user_model()



def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            next_page = request.POST["next"] or '/'
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                #next_page = request.GET.get("next", "/") 
                messages.info(request, f"Logged in as {user.username}")
                response = HttpResponse()
                response.headers['HX-Redirect'] = next_page
                return response
            else:
                return HttpResponse("Username or Password didn’t match")
        return render(request, 'users/login.html')
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
 
def logout(request):
    auth_logout(request)
    messages.info(request, "Logged out")
    next_page = request.GET.get("next") or "/"
    return redirect(next_page)
    
    
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                messages.success(request, f"Signed up as {user.username}")
                response = HttpResponse()
                response.headers['HX-Redirect'] = '/'
                return response
            return render(request, 'users/partials/signup-form.html', {'form': form})
        else:
            form = SignUpForm()
        return render(request, 'users/signup.html', {'form': form})
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
    
def check_username_availability(request):
    if request.method == "POST":
        username=request.POST["username"]
        if username == "":
            return HttpResponse("")
        
        user_obj=CustomUser.objects.filter(username=username)
        if user_obj.exists():
            return HttpResponse("Username is already taken, please select another one.")
        return HttpResponse("")
    return HttpResponse("Method not allowed")
        

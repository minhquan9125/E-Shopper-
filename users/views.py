
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .form import CustomerUserForm
from django.contrib.auth import authenticate ,logout,login
from django.contrib.auth.forms import AuthenticationForm


def register_view(request):
    if request.method == 'POST':
        form = CustomerUserForm(request.POST , request.FILES)
        if form.is_valid():
            user= form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            user.is_superuser = False
            user.is_staff = False

            user.save()

            return HttpResponse("Đăng ký thành công , đã gửi mail.")
    else :
        form=CustomerUserForm()

    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            user = form.get_user()
            login(request, user)                
            request.session['user_id'] = user.id
            return redirect('home') 
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render,redirect
from django.contrib import messages
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
            login(request, user)
            if request.session.get('cart'):
                from cart.views import complete_order
                try:
                    complete_order(request, user)
                except Exception:
                    messages.error(request, 'Tài khoản đã tạo. Không gửi được email đơn hàng; hãy thử lại tại Checkout.')
                    return redirect('checkout_view')
                request.session['order_success'] = True
                return redirect('checkout_view')
            return redirect('home')
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

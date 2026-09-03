from django.shortcuts import render,redirect
from users.models import Country

def update_user_view(request):
    user = request.user
    countries = Country.objects.all()
    if request.method == 'POST':
        username=request.POST.get('username')
        user.email=request.POST.get('email')
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.address=request.POST.get('address')
        user.country_id=request.POST.get('id_country')
        user.phone=request.POST.get('phone')
        user.avatar=request.FILES.get('avatar')
        user.save()
        return redirect('update_user_view')
    return render(request, 'update.html', {'countries': countries})

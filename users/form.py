from django import forms
from .models import CustomerUser
from django.core.exceptions import ValidationError

class CustomerUserForm (forms.ModelForm ):
    password = forms.CharField(widget=forms.PasswordInput, max_length=10)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomerUser
        fields = ['username',"password", "confirm_password", 'email', 'first_name', 'last_name', 'avatar', 'id_country']

        def clean_username(self):
            username= self.clean_data.get('username')
            if CustomerUser.objects.filter(username=username).exists():
                raise ValidationError("username đã tồn tại")
            return username

        def clean_email(self):
            email=self.clean_email.get('gmail')
            if CustomerUser.objects.filter(email=email).exists():
                raise ValidationError("email đã tồn tại")
            return email
        
        def clean_avatar(self):
            avatar=self.clean_avatar.get('avatar')
            if avatar:
                if avatar.size > 1024 *1024 :
                    raise ValidationError("ảnh phải nhỏ hơn 1 MB")
            if not avatar.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    raise ValidationError("ảnh phải đúng định dạng ")
            return avatar     

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password and confirm_password and password != confirm_password:
                raise ValidationError("Mật khẩu xác nhận không khớp.")
            return cleaned_data
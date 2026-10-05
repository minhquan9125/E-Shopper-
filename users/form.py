from django import forms

from .models import CustomerUser


class CustomerUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Mật khẩu')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Nhập lại mật khẩu')

    class Meta:
        model = CustomerUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 'phone', 'address',
            'avatar', 'id_country',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomerUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email này đã được đăng ký. Hãy đăng nhập.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Mật khẩu nhập lại chưa khớp.')

        return cleaned_data

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 1024 * 1024:
            raise forms.ValidationError('Ảnh phải nhỏ hơn 1 MB.')
        if avatar and not avatar.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise forms.ValidationError('Ảnh phải có định dạng PNG hoặc JPG.')
        return avatar

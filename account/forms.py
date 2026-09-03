# from django import forms
# from django.contrib.auth import get_user_model


# User = get_user_model()

# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'address', 'id_country', 'phone', 'avatar']
        
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
#             'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
#             'id_country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
#             # 'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
#             'avatar': forms.FileInput(attrs={'class': 'form-control'}),
#         }
from django import forms 
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'avatar']
        widgets = {
            'password': forms.PasswordInput()
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user        
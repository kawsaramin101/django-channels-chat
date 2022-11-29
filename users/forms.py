from django import forms
from django.forms import TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class SignUpForm(UserCreationForm):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['username'].widget = TextInput(attrs={"placeholder": "Username"})
        self.fields['password1'].help_text = _('At least 8 character long')
        self.fields['password1'].widget = PasswordInput(attrs={"placeholder": "Password"})
        self.fields['password2'].help_text = _('Same as before.')
        self.fields['password2'].widget = PasswordInput(attrs={"placeholder": "Password confirmation"})
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        
        labels = {
            'password1': _('Password'),
            'password2': _("Password Confirmation"),
        }



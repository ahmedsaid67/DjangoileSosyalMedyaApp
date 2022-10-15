
from attr import attr
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class":"bg-gray-200 mb-2 shadow-none dark:bg-gray-800"
        })
        self.fields["email"].widget.attrs.update({
            "class":"bg-gray-200 mb-2 shadow-none dark:bg-gray-800"
        })
        self.fields["password1"].widget.attrs.update({
            "class":"bg-gray-200 mb-2 shadow-none dark:bg-gray-800"
        })
        self.fields["password2"].widget.attrs.update({
            "class":"bg-gray-200 mb-2 shadow-none dark:bg-gray-800"
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

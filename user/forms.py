from django.contrib.auth.forms import UserChangeForm
from home.models import UserProfile
from django.forms.widgets import EmailInput, FileInput, Select, TextInput
from django.contrib.auth.models import User
from django import forms
from kurumsal.models import Comment


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'username', 'email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder': 'username'}),
            'email'     : EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),
            'first name': TextInput(attrs={'class': 'input','placeholder': 'first name'}),
            'Last name' : TextInput(attrs={'class': 'input', 'placeholder': 'last name' }),
        }
CITY = [
('Istanbul', 'Istanbul'),
('Ankara', 'Ankara'),
('Izmir', 'Izmir'),
]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city','country', 'image')
        widgets = {
                'phone' : TextInput(attrs={'class': 'input','placeholder': 'phone'}),
                'address': TextInput (attrs={'class': 'input','placeholder':'address'}),
                'city' : Select(attrs={'class': 'input', 'placeholder':'city'},choices=CITY),
                'country': TextInput(attrs={'class': 'input', 'placeholder': 'country' }),
                'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['subject', 'comment', 'rate']



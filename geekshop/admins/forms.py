from django import forms

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserAdminRegisterForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)


class UserAdminUpdateDeleteForm(UserProfileForm):
    pass

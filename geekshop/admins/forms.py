from django import forms

from products.models import ProductCategory
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserAdminRegisterForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)


class UserAdminUpdateDeleteForm(UserProfileForm):
    pass


class CategoryForm(forms.ModelForm):
    discount = forms.IntegerField(widget=forms.NumberInput(), label='discount', required=False,
                                  min_value=0, max_value=50)

    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'discount', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

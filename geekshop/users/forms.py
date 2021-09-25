from django.contrib.auth.forms import forms, AuthenticationForm, UserCreationForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    # username = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter your username'}))
    # password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter your password'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeate your password'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def clean(self):
        cleaned_data = super(self.__class__, self).clean()
        fields_str = str(
                (self.cleaned_data.get('username').lower(),
                self.cleaned_data.get('email').lower(),
                self.cleaned_data.get('first_name').lower(),
                self.cleaned_data.get('last_name').lower()))
        if 'pupkin' in fields_str:
            raise forms.ValidationError('PUPKIN in da house!!!')
        return cleaned_data
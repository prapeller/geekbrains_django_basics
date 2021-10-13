from django.contrib.auth.forms import forms, AuthenticationForm, UserCreationForm, UserChangeForm

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
        fields = ('username', 'email', 'first_name', 'last_name', 'age', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeate your password'

        for field_name, field in self.fields.items():
            if field_name != 'image':
                field.widget.attrs['class'] = 'form-control py-4'

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        fields_str = str(
            (self.cleaned_data.get('username').lower(),
             self.cleaned_data.get('email').lower(),
             self.cleaned_data.get('first_name').lower(),
             self.cleaned_data.get('last_name').lower()))
        if 'pupkin' in fields_str:
            raise forms.ValidationError('PUPKIN in da house!!!')
        return cleaned_data


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta():
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            if field_name != 'image':
                field.widget.attrs['class'] = 'form-control py-4'

    def clean_image(self):
        data = self.cleaned_data['image']
        if data and data.size > 1048576:
            raise forms.ValidationError('Size of image can not be more then 1 MB')
        return data

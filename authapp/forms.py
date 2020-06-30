from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm
import django.forms as forms

from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = (
            'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'age', 'avatar'
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''


class ShopUserUpdateForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = (
            'username', 'password', 'email', 'first_name',
            'last_name', 'age', 'avatar'
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.widget = forms.HiddenInput()
            else:
                field.widget.attrs['class'] = f'form-control {field_name}'
                field.help_text = ''
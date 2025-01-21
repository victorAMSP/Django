import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def add_attr(field, attr_name, attr_new_val):
    if field:
        existing = field.widget.attrs.get(attr_name, '')
        field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    if field:
        add_attr(field, 'placeholder', placeholder_val)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        error_messages={'required': 'Username is required'},
        label='Username',
        required=True,
        help_text=(
            'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'
        ),
    )
    first_name = forms.CharField(
        error_messages={'required': 'First name is required'},
        label='First name',
        required=True,
    )
    last_name = forms.CharField(
        error_messages={'required': 'Last name is required'},
        label='Last name',
        required=True,
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
        help_text='The e-mail must be valid.',
        required=True,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': 'Confirm password is required'},
        label= 'Confirm password',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': 'Password is required'
        },
        help_text=(
            "Password must have at least one uppercase letter, "
            "one lowercase letter, one number, and at least 8 characters."
        ),
        label= 'Password',
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'confirm_password',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Your username',
            'email': 'Your e-mail',
            'first_name': 'Ex.: Jhon',
            'last_name': 'Ex.: Doe',
            'password': 'Your password',
            'confirm_password': 'Repeat your password'
        }
        for field_name, placeholder in placeholders.items():
            add_placeholder(self.fields.get(field_name), placeholder)

        for field in self.fields.values():
            add_attr(field, 'class', 'form-control')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Email is required.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise ValidationError("Username is required.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        if " " in username:
            raise ValidationError("Username cannot contain spaces.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if not password or not confirm_password:
            raise ValidationError("Password and confirm password are required.")

        if password != confirm_password:
            raise ValidationError({
                'confirm_password': "Passwords do not match."
            })

        if password and not re.fullmatch(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$',
            password
        ):
            raise ValidationError({
                'password': (
                    "Password must be at least 8 characters long, include an uppercase letter, "
                    "a lowercase letter, a number, and a special character (!@#$%^&*(), etc.)."
                )
            })

        return cleaned_data
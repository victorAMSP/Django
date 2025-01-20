from django import forms
from django.contrib.auth.models import User

def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: Jhon')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_attr(self.fields['username'], 'css', 'a-css-class')
    
    password = forms.CharField(
        required= True,
        widget= forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages= {
            'required': 'Password must be not empty'
        },
        help_text= (
            'Passworld must have at least one uppercase letter,'
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.'
        )
    )
    password2 = forms.CharField(
        required=True,
        widget= forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
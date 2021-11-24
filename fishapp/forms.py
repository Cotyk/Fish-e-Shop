from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'buying_type', 'region', 'location', 'section', 'paying_type', 'first_name', 'last_name', 'phone',
            'address', 'comment'
        )


class LoginForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = 'Логін'
        self.fields["password"].label = 'Пароль'
        self.fields['password'].help_text = mark_safe(
            f"""<hr><strong><span style="color:green;">*</span> Не маєте акаунту? <a href="{reverse('register')}">Зареєструйтесь</a>.</strong>"""
        )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Користувач з логіном {username} не знайдений в системі.')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Невірний пароль")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = 'Логін'
        self.fields["password"].label = 'Пароль'
        # self.fields['password'].help_text = mark_safe(
        #     '<hr><strong><span style="color:green;">*</span> Використовуйте дані з Вашого акаунту borntofish.org</strong>'
        # )

    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Користувач з логіном {username} вже існує.')
        elif User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Користувач з поштою {email} вже існує.')
        elif password != password2:
            raise forms.ValidationError(f'Паролі не збігаються.')

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

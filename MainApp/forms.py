from django.forms import ModelForm, TextInput, CharField, PasswordInput
from MainApp.models import Snippet
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class SnippetForm(ModelForm):
   class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code', 'is_public']
        widgets = {
            'name': TextInput(attrs={
                "class":       "form-control form-control-lg",
                'placeholder': 'Название сниппета'}),

        }
        labels = {
            'name': 'Название',
            'lang': 'Язык',
            'code': 'Код',
            'is_public': 'Публичный'
        }


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    password1 = CharField(label="password", widget=PasswordInput)
    password2 = CharField(label="password confirm", widget=PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username)>3:
            return username
        raise ValidationError("Too short username")

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 == pass2:
            return pass2
        raise ValidationError("Пароли не совпадают или пустые")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

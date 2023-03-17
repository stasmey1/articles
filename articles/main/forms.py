from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput
from .models import Post, Comment
from django.contrib.auth.models import User


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('unregistered_author', 'title', 'text', 'image',)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'unregistered_author')


class UserRegistrationForm(ModelForm):
    password = CharField(label='Password', widget=PasswordInput)
    password2 = CharField(label='Repeat password', widget=PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Passwords don\'t match.')
        return cd['password2']

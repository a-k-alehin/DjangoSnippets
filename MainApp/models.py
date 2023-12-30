from django.db import models
from django.contrib.auth.models import User

LANGS = (
    ('py', 'Python'),
    ('js', 'JavaScript'),
    ('cpp', 'C++')
)


class Language(models.Model):
    shortname = models.CharField(max_length=10)
    fullname =  models.CharField(max_length=50)

    def __repr__(self):
        return f'{self.shortname}'
    def __str__(self):
        return repr(self)


class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANGS)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    language = models.ForeignKey(to=Language, on_delete=models.PROTECT, blank=True, null=True)

    def __repr__(self):
        return f'{self.name} {self.language}'
    def __str__(self):
        return repr(self)


class Comment(models.Model):
    text = models.TextField(max_length=1000)
    creation_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    snippet = models.ForeignKey(to=Snippet, on_delete=models.CASCADE, related_name="comments")

    def __repr__(self):
        return f'{self.author} {self.creation_date} {self.snippet}'
    def __str__(self):
        return repr(self)

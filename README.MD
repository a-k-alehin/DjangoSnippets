install requirements:
`pip install -r requirements.txt`

run project:
`python manage.py runserver`

run django-extensions console:
`python manage.py shell_plus --ipython`

    python manage.py shell_plus --ipython
    user = User.objects.create_user('user', password='user')
    user.is_staff = True
    user.save()

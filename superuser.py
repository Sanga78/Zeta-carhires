import subprocess

try:
    subprocess.check_call(
        'echo "from django.contrib.auth.models import User; '
        'User.objects.create_superuser(\'noel\', \'sawenoelt01@gmail.com\', \'Tumbaisawe79#\')" | '
        'python manage.py shell',
        shell=True
    )
    print("Superuser created successfully")
except subprocess.CalledProcessError as e:
    print(f"Error creating superuser: {e}")
    pass
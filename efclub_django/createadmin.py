from django.contrib.auth.models import User
User.objects.create_superuser('efadmin', '', 'pass')

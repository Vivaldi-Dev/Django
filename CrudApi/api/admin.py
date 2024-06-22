from django.contrib import admin

from .models import User
from .models import UserTask

admin.site.register(User)
admin.site.register(UserTask)

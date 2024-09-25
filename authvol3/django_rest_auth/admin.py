from django.contrib import admin
from .models import User,OnetimePassword
# Register your models here.


admin.site.register(User)
admin.site.register(OnetimePassword)
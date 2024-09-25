from django.contrib import admin
from .models import carlist
from .models import Showroomlist
from .models import Review

admin.site.register(carlist)
admin.site.register(Showroomlist)
admin.site.register(Review)
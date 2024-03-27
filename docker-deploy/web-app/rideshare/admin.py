from django.contrib import admin

from .models import Ride, Driver, Sharer

admin.site.register(Ride)
admin.site.register(Driver)
admin.site.register(Sharer)


from django.contrib import admin
from .models import Event
from .models import Ticket

admin.site.register(Event)
admin.site.register(Ticket)


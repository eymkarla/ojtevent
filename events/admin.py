from django.contrib import admin
from .models import Event, Invite, Member
# Register your models here.
admin.site.register(Event)
admin.site.register(Invite)
admin.site.register(Member)
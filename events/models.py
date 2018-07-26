from django.conf import settings
from django.db import models
from users.models import User
from secrets import token_urlsafe 
from .utils import user_media_path
from uuid import uuid4

class Event(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to=user_media_path, null=True, blank=True)

    venue = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    date_updated = models.DateTimeField(auto_now=True)

    description = models.TextField()

    archive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

class Invite(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=120)
    is_member = models.BooleanField(default=False)
    is_tokened = models.BooleanField(default=False)

    def generate_token(self):
        return uuid4().hex

    def __str__(self):
        return "{}-invite".format(self.email)

    def save(self, *args, **kwargs):
        if not self.id:
            self.token=self.generate_token()
        return super(Invite, self).save(*args, **kwargs)

class Member(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='events')
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return "{} in {}".format(self.member, self.event)
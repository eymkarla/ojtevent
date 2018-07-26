from django import forms
from annoying.functions import get_object_or_None
from django.conf import settings
from users.models import User
from .models import Event, Invite
from django.forms import ModelForm
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

class PostForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'image', 'category', 'venue', 'date', 'time', 'description']

class InviteForm(forms.Form):

    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={'class' : 'form-control sign-up-input'}))

    def __init__(self, *args, **kwargs):
        self.event_id = kwargs.pop('event_id', None)
        return super(InviteForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        data.update({'event': Event.objects.get(id=self.event_id)})

        post = Invite.objects.create(**data)

        return post


    def send_invite(self, request, host, email, event):
        email = self.cleaned_data.get('email')
        new_invite = Invite.objects.create(email=email, event=event)
        token = new_invite.token
        extended_link = request.build_absolute_uri(reverse('accept_invite', args=(token,)))

        full_message = ("{} has invited you to join '{}' event! \n" 
                "Click the link to join the event. \n{}").format(request.user.first_name, event, extended_link)
             
        send_mail(
            'Invitation Request',
            full_message,
            settings.EMAIL_HOST,
            [email],
            fail_silently=False,
        )
        new_invite.event = event
        new_invite.save()
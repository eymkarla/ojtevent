from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, InviteForm
from .models import Event, Invite, Member
from users.models import User
from django.contrib.auth import login, authenticate
from users.forms import UserForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail

def index(request):
    context = {}
    context['posts'] = Event.objects.filter(archive=False).order_by('-date_updated')
    context['name'] = 'Posts'
    return render(request, 'events/index.html', context)

def createpost(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(files=request.FILES, data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.date_created = timezone.now()
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'events/createpost.html', {"form": form})
    else:
        return render(request, 'events/createpost.html', {"form": form})

def editpost(request, event_id):
    template = 'blogs/editpost.html'
    post = get_object_or_404(Post, id=event_id)
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form =PostForm(instance=post)
        args = {'form':form}
        return render(request, 'events/editpost.html', args)


def post_details(request, event_id):
    template = 'events/post_details.html'
    
    post= get_object_or_404(Event, id=event_id)
    context = {'post':post,}

    return render(request, template, context)

def search_form(request):
   return render(request, 'events/index.html')

def search(request):
   error = False
   
   if 'q' in request.GET:
       q = request.GET['q']
       if not q:
           error = True
       else:
           posts = Event.objects.filter( Q(title__icontains=q) | Q(category__icontains=q) | Q(description__icontains=q))
           return render(request, 'events/search_results.html', {'posts':posts, 'query':q})
   
   
   return render(request, 'events/index.html', {'error': error})

def search_result(request, event_id):
   template = 'events/search_result.html'
  
   post= get_object_or_404(Event, id=event_id)
   context = {'post':post,}
   return render(request, template, context)

def archivepost(request, event_id):
    post = get_object_or_404(Event, id=event_id, author=request.user)
    post.archive=True
    post.save()
    return HttpResponseRedirect(reverse('index'))

def unarchivepost(request, event_id):
    post = get_object_or_404(Event, id=event_id, author=request.user)
    post.archive=False
    post.save()
    return HttpResponseRedirect(reverse('archivelist'))

def archivelist(request):
    context = {}
    context['posts'] = Event.objects.filter(archive=True)
    context['name'] = 'Posts'
    return render(request, 'events/archivelist.html', context)

def invite_email(request, event_id):
    if not request.method == "POST": raise Http404

    data = request.POST
    event = get_object_or_404(Event,pk=event_id)

    form = InviteForm(data, event_id=event_id)
    if form.is_valid():
        host = request.get_host()
        invite = form.save()
        email = form.data.get('email')
        form.send_invite(request, host, email, event)

        return render(request, 'events/index.html')
    else:
      return render(request, 'events/index.html')

def accept_invite(request, token):
      invite = get_object_or_404(Invite, token=token)
      if not invite.is_tokened:
          
          user = User.objects.filter(email=invite.email)
          if user.exists():
              _create_event_member(user[0], invite.event)
              invite.is_tokened = True
              invite.save()
              login(request, user[0])
              return redirect( 'post_details', invite.event.id)
          else:
              form = UserForm()
              if request.method =='POST':
                  form = UserForm(request.POST)
                  if form.is_valid():
                      password = form.cleaned_data['password']
                      email = form.cleaned_data['email']
                      member = form.save()
                      _create_event_member(member, invite.event)
                      invite.is_tokened = True
                      invite.save()
                      user = authenticate(email=email, password=password)

                      if user is not None:
                          login(request, user)
                          return redirect( 'post_details', invite.event.id)
              return render (request, 'users/signup.html', {'form': form })
      else:
          raise Http404("Token does not exist")
          
        



def _create_event_member(member, event):
    event_member = Member()
    event_member.member= member
    event_member.event= event
    event_member.save()
    return member

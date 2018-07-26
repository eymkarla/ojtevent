from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('createpost/', views.createpost, name='createpost'),
    path('index/', views.index, name='index'),
    path('post_details/<int:event_id>/', views.post_details, name='post_details'),
    path('editpost/<int:event_id>/', views.editpost, name='editpost'),
    path('archivepost/<int:event_id>/', views.archivepost, name='archivepost'),
    path('archivelist/', views.archivelist, name='archivelist'),
    path('unarchivepost/<int:event_id>/', views.unarchivepost, name='unarchivepost'),
    path('search_form/', views.search_form, name='search_form'),
	path('search/', views.search, name="search"),
	path('search_result/<int:event_id>/', views.search_result, name='search_result'),
    path('invite_email/<int:event_id>/', views.invite_email, name='invite_email'),
    path('events/validate/<str:token>', views.accept_invite, name="accept_invite"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
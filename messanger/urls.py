from django.urls import path
from . import views
urlpatterns = [
   	path('message/', views.Inbox, name='inbox'),
   	path('directs/<username>', views.Directs, name='directs'),
   	path('new/<username>', views.NewConversation, name='newconversation'),
   	path('send/', views.SendDirect, name='send_direct'),
	path('new/', views.UserSearch, name='usersearch'),
]
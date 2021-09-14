from django.urls import path
from . import views
from notification.views import DeleteNotification


urlpatterns = [
   	path('', views.ShowNOtificationsStudent, name='show-notifications-student'),
	path('', views.ShowNOtificationsTeacher, name='show-notifications-teacher'),
	   
   	path('<noti_id>/delete', DeleteNotification, name='delete-notification'),

]
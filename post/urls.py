from django.urls import path
from . import views

urlpatterns = [
    path('post-list', views.post_list, name="post_list"),
    path('create-post', views.post_create_view, name='post_create'),
    path('comment-create/<int:pk>/', views.comment_create_view.as_view(), name="comment_create"),

    path('create-post-teacher', views.post_create_view_teacher, name='create_post_teacher'),
    path('comment-create-teacher/<int:pk>/', views.comment_create_view_teacher.as_view(), name="comment_create_teacher"),
]
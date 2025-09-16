from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.home_feed, name='home_feed'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),

    # Likes
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),

    # Comments
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),

    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

]

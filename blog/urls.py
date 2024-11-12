from django.urls import path

from blog.views import index,post_single

urlpatterns = [
    path('', index),
    path('posts/<int:post_id>/', post_single,name='post_detail'),
]

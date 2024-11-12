from django.urls import path

from blog.views import index,post_single

urlpatterns = [
    path('', index),
    path('post/', post_single),
]

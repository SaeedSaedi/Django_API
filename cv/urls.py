from django.urls import path

from cv.views import index

urlpatterns = [
    path('', index),
]

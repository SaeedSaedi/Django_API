from django.urls import path

from blog.views import blog_search, index, post_single

app_name = "blog"

urlpatterns = [
    path("", index, name="index"),
    path("posts/<int:post_id>/", post_single, name="post_detail"),
    path("category/<str:cat_name>/", index, name="category"),
    path("author/<str:username>/", index, name="author"),
    path("search/", blog_search, name="search"),
]

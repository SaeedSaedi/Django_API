from django.contrib import admin
from blog.models import Category, Post
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = "created_at"
    empty_value_display = "-empty-"
    list_display = ("title", "author", "status", "created_at")
    search_fields = ("title", "content")
    summernote_fields = ("content",)


admin.site.register(Category)
admin.site.register(Post, PostAdmin)

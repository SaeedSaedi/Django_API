from django.contrib import admin
from blog.models import Category, Post, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = "created_at"
    empty_value_display = "-empty-"
    list_display = ("title", "author", "status", "created_at")
    search_fields = ("title", "content")
    summernote_fields = ("content",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "created_at")
    list_filter = ("approved", "created_at")
    search_fields = ("name", "email", "message")
    actions = ["approve_comments"]


admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)

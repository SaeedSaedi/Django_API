from django.contrib import admin
from blog.models import Category, Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    empty_value_display = "-empty-"
    list_display = ("title", "author", "status", "created_at")
    search_fields = ("title", "content")


admin.site.register(Category)
admin.site.register(Post, PostAdmin)

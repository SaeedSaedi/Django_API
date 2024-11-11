from django.contrib import admin
from blog.models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    empty_value_display = "-empty-"
    list_display = ("title","created_at")
    search_fields = ("title","content")
    
admin.site.register(Post,PostAdmin)
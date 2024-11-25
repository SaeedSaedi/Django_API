from django.contrib import admin
from landing.models import Contact, Newsletter

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject")


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("email",)


admin.site.register(Contact, ContactAdmin)
admin.site.register(Newsletter, NewsletterAdmin)

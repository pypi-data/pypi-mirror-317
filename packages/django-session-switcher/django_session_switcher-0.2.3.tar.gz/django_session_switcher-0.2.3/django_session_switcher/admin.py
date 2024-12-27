from django.contrib import admin
from .models import SessionUser


@admin.register(SessionUser)
class SessionUserAdmin(admin.ModelAdmin):
    fields = ["username", "password"]
    list_display = ('username',)
    search_fields = ('username',)

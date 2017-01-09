from django.contrib import admin

from .models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    list_display = ('user', 'verb', 'target', 'created')
    search_fields = ('verb',)

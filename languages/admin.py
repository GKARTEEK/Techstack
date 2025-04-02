from django.contrib import admin
from .models import Language, Topic

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_featured', 'created_at')
    list_filter = ('is_featured',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'language')
    list_filter = ('language',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
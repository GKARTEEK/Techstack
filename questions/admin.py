from django.contrib import admin
from .models import Question, Category, Bookmark

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'difficulty', 'is_approved', 'created_by', 'created_at')
    list_filter = ('difficulty', 'is_approved', 'language', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('topics',)
    actions = ['approve_questions']
    
    def approve_questions(self, request, queryset):
        queryset.update(is_approved=True)
    approve_questions.short_description = "Approve selected questions"

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created_at')
    list_filter = ('user',)
from django.shortcuts import render
from django.db.models import Count, Q
from languages.models import Language
from questions.models import Question

def home(request):
    featured_languages = Language.objects.filter(is_featured=True)[:6]
    all_languages = Language.objects.all()
    trending_questions = Question.objects.filter(is_approved=True).annotate(
        bookmark_count=Count('bookmarks')
    ).order_by('-bookmark_count', '-created_at')[:5]
    
    context = {
        'featured_languages': featured_languages,
        'all_languages': all_languages,
        'trending_questions': trending_questions,
    }
    return render(request, 'core/home.html', context)

def search(request):
    query = request.GET.get('q', '')
    languages = []
    questions = []
    
    if query:
        languages = Language.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        questions = Question.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(language__name__icontains=query)
        ).filter(is_approved=True)
    
    context = {
        'query': query,
        'languages': languages,
        'questions': questions,
    }
    return render(request, 'core/search.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

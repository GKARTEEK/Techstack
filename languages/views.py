from django.shortcuts import render, get_object_or_404
from .models import Language, Topic
from questions.models import Question

def language_list(request):
    languages = Language.objects.all()
    return render(request, 'languages/language_list.html', {'languages': languages})

def language_detail(request, slug):
    language = get_object_or_404(Language, slug=slug)
    topics = language.topics.all()
    easy_questions = Question.objects.filter(language=language, difficulty='easy', is_approved=True)
    medium_questions = Question.objects.filter(language=language, difficulty='medium', is_approved=True)
    hard_questions = Question.objects.filter(language=language, difficulty='hard', is_approved=True)
    
    context = {
        'language': language,
        'topics': topics,
        'easy_questions': easy_questions,
        'medium_questions': medium_questions,
        'hard_questions': hard_questions,
    }
    return render(request, 'languages/language_detail.html', context)

def topic_detail(request, lang_slug, topic_slug):
    language = get_object_or_404(Language, slug=lang_slug)
    topic = get_object_or_404(Topic, slug=topic_slug, language=language)
    questions = Question.objects.filter(topics=topic, is_approved=True)
    
    context = {
        'language': language,
        'topic': topic,
        'questions': questions,
    }
    return render(request, 'languages/topic_detail.html', context)
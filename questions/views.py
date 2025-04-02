from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Question, Bookmark, Category
from .forms import QuestionForm, QuestionFilterForm

def question_list(request):
    filter_form = QuestionFilterForm(request.GET)
    questions = Question.objects.filter(is_approved=True)
    
    if filter_form.is_valid():
        difficulty = filter_form.cleaned_data.get('difficulty')
        category = filter_form.cleaned_data.get('category')
        language = filter_form.cleaned_data.get('language')
        
        if difficulty:
            questions = questions.filter(difficulty=difficulty)
        if category:
            questions = questions.filter(category=category)
        if language:
            questions = questions.filter(language=language)
    
    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'filter_form': filter_form,
        'page_obj': page_obj,
    }
    return render(request, 'questions/question_list.html', context)

def question_detail(request, slug):
    question = get_object_or_404(Question, slug=slug, is_approved=True)
    is_bookmarked = False
    
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, question=question).exists()
    
    related_questions = Question.objects.filter(
        language=question.language, 
        is_approved=True
    ).exclude(id=question.id)[:5]
    
    context = {
        'question': question,
        'is_bookmarked': is_bookmarked,
        'related_questions': related_questions,
    }
    return render(request, 'questions/question_detail.html', context)

@login_required
def bookmark_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, is_approved=True)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, question=question)
    
    if not created:
        bookmark.delete()
        messages.success(request, 'Bookmark removed.')
    else:
        messages.success(request, 'Question bookmarked successfully.')
    
    return redirect('question_detail', slug=question.slug)

@login_required
def submit_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Your question has been submitted for review.')
            return redirect('home')
    else:
        form = QuestionForm()
    
    return render(request, 'questions/submit_question.html', {'form': form})
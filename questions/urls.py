from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('submit/', views.submit_question, name='submit_question'),  # ✅ Keep this BEFORE the slug path
    path('bookmark/<int:question_id>/', views.bookmark_question, name='bookmark_question'),
    path('<slug:slug>/', views.question_detail, name='question_detail'),
    path('ajax/load-topics/', views.load_topics, name='ajax_load_topics'),

]

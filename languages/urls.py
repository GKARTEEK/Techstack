from django.urls import path
from . import views

urlpatterns = [
    path('', views.language_list, name='language_list'),
    path('<slug:slug>/', views.language_detail, name='language_detail'),
    path('<slug:lang_slug>/topic/<slug:topic_slug>/', views.topic_detail, name='topic_detail'),
]
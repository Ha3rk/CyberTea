from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('categories/', views.category_list, name='category_list'),
    path('about/', views.about, name='about'),
    path('incident_stats/', views.incident_stats, name='incident_stats'),
    
    # New path for summarizing articles
    path('get-article-summary/', views.summarize_article, name='get_article_summary'),
    
    # Authentication
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

      
      ]
    
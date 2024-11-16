from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('categories/', views.category_list, name='category_list'),
    path('about/', views.about, name='about'),
    path('incident_stats/', views.incident_stats, name='incident_stats'),
    
    # New path for summarizing articles
    path('summarize/', views.summarize_article, name='summarize_article'),    
    # Authentication
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

     path('logout/', views.logout_view, name='logout'),
   #path('chat/', views.chat_view, name='chat'),
      
      ]
    
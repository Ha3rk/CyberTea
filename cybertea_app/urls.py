from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('about/', views.contact, name='contact'),
    path('about/', views.resource, name='resource'),
    path('about/', views.trending, name='trending'),
    path('forums/', views.forums, name='forums'),
    path("detail/<slug>/", views.detail, name="detail"),
    path("posts/<slug>/", views.posts, name="posts"),
    path("create_post/", views.create_post, name="create_post"),
    path("latest_posts/", views.latest_posts, name="latest_posts"),
    path("search/", views.search_result, name="search_result"),
    path('incident_stats/', views.incident_stats, name='incident_stats'),
    
    
    # New path for summarizing articles
    path('summarize/', views.summarize_article, name='summarize_article'),    
    # Authentication
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

     path('logout/', views.logout_view, name='logout'),
   #path('chat/', views.chat_view, name='chat'),
      
      ]
    
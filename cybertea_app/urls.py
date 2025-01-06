from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('about/', views.contact, name='contact'),
    path('resource/', views.resource, name='resource'),
    path('about/', views.trending, name='trending'),
    path('forums/', views.forums, name='forums'),
    path("detail/<slug>/", views.detail, name="detail"),
    path("posts/<slug>/", views.posts, name="posts"),
    path("create_post/", views.create_post, name="create_post"),
    path("latest_posts/", views.latest_posts, name="latest_posts"),


    # Incident stats display
    path('recent-cves/', views.recent_cves, name='recent_cves'),
    path('cve/<str:cve_id>/', views.cve_details, name='cve_details'),
    
    
    # New path for summarizing articles
    path('summarize/', views.summarize_article, name='summarize_article'),    
    # Authentication
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    #search forum
    path('search/', views.forum_search, name='forum_search'),

      ]


#def bad_request(request, exception):
#    return render(request, 'cyberevents/error_400.html', status=400)

##def server_error(request):
 #   return render(request, 'cyberevents/error_500.html', status=500)

#    #Error handlers
#handler400 = 'cybertea_project.urls.bad_request'
#handler500 ="ybertea_project.urls.server_error"
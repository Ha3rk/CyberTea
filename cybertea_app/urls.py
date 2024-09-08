from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('base/', views.base, name= 'base'),
    path('categories/', views.category_list, name='category_list'),
    path('about/', views.about, name= 'about'),

]
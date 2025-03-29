"""
URL configuration for AjoloEnergy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('articles/', views.article_list_json, name='articles_view'),
<<<<<<< HEAD
    path('article_consume/', views.article_consume, name='article_consume' ),
    path('increase_consumition/', views.increase_consumption),
    path('decrease_consumition/', views.decrement_last_increase),
    path('get_consumition/', views.get_consumicion),
=======
    path('article_consume/', views.article_consume, name='article_consume'),
    path('week_article_consume/', views.weekly_article_consume, name='weekly_article_consume'),
    path('yearly_article_consume/', views.yearly_article_consume, name='yearly_article_consume'),
>>>>>>> 37a585936c16fdbb8c668a8b440c791426100f73
]
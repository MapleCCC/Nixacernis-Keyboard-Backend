from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transliterate/<str:raw_key_list>/',
         views.transliterate, name='transliterate'),
    path('increment/<str:chosen_chinese_word>/',
         views.increment, name='increment'),
]

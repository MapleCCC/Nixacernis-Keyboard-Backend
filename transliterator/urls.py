from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:chinese_word>', views.detail, name="detail"),
    path('transliterate/<str:raw_key_list>/',
         views.transliterate, name='transliterate'),
    path('increment/<str:chinese_word>/', views.increment, name='increment')
]

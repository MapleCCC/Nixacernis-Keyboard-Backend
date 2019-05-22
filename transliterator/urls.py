from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:chinese_word>/', views.detail, name="detail"),
    path('transliterate/<str:raw_key_list>/<int:offset>/',
         views.transliterate_request_handler, name='transliterate'),
    path('transliterate/<str:raw_key_list>/',
         views.transliterate_request_handler, name='transliterate_fallback'),
    path('demo/<str:raw_key_list>/<int:offset>/', views.demo, name="demo"),
    path('increment/<str:chinese_word>/', views.increment, name='increment')
]

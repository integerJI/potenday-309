from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('challenges/', views.ChallengeCreate.as_view(), name='challenge-create'),
    path('challenges/<int:pk>/', views.ChallengeView.as_view(), name='challenge-detail'),
    path('images/', views.ImageList.as_view(), name='challenge-image-list'),
    path('images/<int:pk>/', views.ImageList.as_view(), name='challenge-image-list'),
    path('stamp/<int:pk>/', views.StampList.as_view(), name='challenge-stamp-list'),
]
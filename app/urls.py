from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('sample/', views.getSampleApi, name='getSampleApi'),
    path('challenges/', views.ChallengeListCreateView.as_view(), name='challenge-list-create'),
    path('challenges/<int:pk>/', views.ChallengeRetrieveView.as_view(), name='challenge-retrieve'),
]
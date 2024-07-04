from django.urls import path
from django.http import HttpResponse
from .views import (
    PersonalListView, 
    PersonalDetailView,
    PersonalUpdateView,
    PersonalDeleteView,
    UserPersonalListView,
    PersonalCreateView,
    PostWizard,
    TemplateView
)
from . import views
from .views import PostWizard, FORMS

urlpatterns = [
    path('', PersonalListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPersonalListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PersonalDetailView.as_view(), name='post-detail'),
    path('post/new/', PersonalCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PersonalUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PersonalDeleteView.as_view(), name='post-delete'),
    path('done/', TemplateView.as_view(template_name='blog/done.html'), name='done'),
    path('about/', views.about, name='blog-about')
]


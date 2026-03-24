from django.contrib import admin  # ← これが足りていません！
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('timeline/', views.timeline, name='timeline'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/add/', views.add_content, name='add_content'),
    path('post/<int:pk>/add-sub/', views.add_sub_content, name='add_sub_content'),
    path('sub-content/<int:pk>/edit/', views.edit_sub_content, name='edit_sub_content'),
    path('sub-content/<int:pk>/delete/', views.delete_sub_content, name='delete_sub_content'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
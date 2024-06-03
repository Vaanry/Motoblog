"""blog URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('follow/', views.FollowListView.as_view(), name='follow_index'),
    path(
        'profile/<slug:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<slug:username>/unfollow/',
        views.profile_unfollow,
        name="profile_unfollow"
    ),
    path('', views.BlogListView.as_view(), name='index'),
    path('<int:pk>/delete/', views.DeletePostView.as_view(),
         name='delete_post'),
    path('<int:pk>/edit/', views.EditPostView.as_view(), name='edit_post'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('edit/<slug:username>/', views.EditProfileView.as_view(),
         name='edit_profile'),
    path('create_post/', views.PostCreateView.as_view(), name='create_post'),
    path('create_post/create_location/', views.LocationCreateView.as_view(),
         name='create_location'),
    path('<slug:category_slug>/', views.CategoryListView.as_view(),
         name='category_posts'),
    path('<str:location>/', views.LocationListView.as_view(),
         name='location_posts'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:id>/edit_comment/<int:pk>/', views.edit_comment,
         name='edit_comment'),
    path('<int:id>/delete_comment/<int:pk>/', views.delete_comment,
         name='delete_comment'),

]

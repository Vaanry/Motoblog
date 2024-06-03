from django.urls import path
from . import views

app_name = 'moto'

urlpatterns = [
    path('catalog/', views.CatalogListView.as_view(), name='catalog'),
    #path('<int:pk>/delete/', views.DeleteMotoView.as_view(),
    #     name='delete_moto'),
    path('<int:pk>/edit/', views.EditMotoView.as_view(), name='edit_moto'),
    path('<int:pk>/', views.MotoDetailView.as_view(), name='moto_detail'),
    path('create_moto/', views.MotoCreateView.as_view(), name='create_moto'),
]
from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.choose_mark, name='mark'),
    path('<slug:mark>/', views.price_calculator, name='price'),
]
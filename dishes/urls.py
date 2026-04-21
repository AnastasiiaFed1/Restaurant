from django.urls import path
from . import views

app_name = 'dishes'

urlpatterns = [
    path('', views.dish_list, name='dish_list'),
    path('category/<slug:category_slug>/', views.category_dishes, name='category_dishes'),
    path('dish/<slug:dish_slug>/', views.dish_detail, name='dish_detail'),
]
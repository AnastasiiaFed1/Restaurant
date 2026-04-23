from django.urls import path
from . import views

app_name = 'dishes'

urlpatterns = [
    path('', views.dish_list, name='dish_list'),
    path('category/<int:category_id>/', views.category_dishes, name='category_dishes'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
]
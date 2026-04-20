from django.contrib import admin
from .models import Category, Cuisine, Tag, Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    # Відображення полів у списку всіх страв
    list_display = ('id', 'get_html_photo', 'name', 'category', 'price', 'is_available')
    # Робимо ід та назву клікабельними для переходу до редагування
    list_display_links = ('id', 'name')

    # Зручний інтерфейс для вибору тегів (два вікна зі стрілочками)
    filter_horizontal = ('tags',)

    # Фільтри справа та пошук зверху
    list_filter = ('category', 'cuisine', 'tags', 'is_available')
    search_fields = ('name', 'description')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
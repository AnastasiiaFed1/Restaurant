from django.shortcuts import render, get_object_or_404
from menu.models import Dish, Category, Cuisine


def apply_filters_and_sorting(request, queryset):
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    cuisine_id = request.GET.get('cuisine', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    available = request.GET.get('available', '').strip()
    spiciness = request.GET.get('spiciness', '').strip()
    sort = request.GET.get('sort', '').strip()

    if q:
        queryset = queryset.filter(name__icontains=q)

    if category_id:
        try:
            queryset = queryset.filter(category_id=int(category_id))
        except ValueError:
            pass

    if cuisine_id:
        try:
            queryset = queryset.filter(cuisine_id=int(cuisine_id))
        except ValueError:
            pass

    if min_price:
        try:
            queryset = queryset.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            pass

    if available == '1':
        queryset = queryset.filter(is_available=True)

    if spiciness:
        try:
            queryset = queryset.filter(spiciness=int(spiciness))
        except ValueError:
            pass

    if sort == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort == 'price_desc':
        queryset = queryset.order_by('-price')
    elif sort == 'name_asc':
        queryset = queryset.order_by('name')
    elif sort == 'name_desc':
        queryset = queryset.order_by('-name')
    else:
        queryset = queryset.order_by('name')

    return queryset


def dish_list(request):
    dishes = Dish.objects.select_related('category', 'cuisine').all()
    dishes = apply_filters_and_sorting(request, dishes)

    categories = Category.objects.all().order_by('name')
    cuisines = Cuisine.objects.all().order_by('name')

    context = {
        'dishes': dishes,
        'categories': categories,
        'cuisines': cuisines,
        'current_filters': request.GET,
        'page_title': 'Меню',
    }
    return render(request, 'dishes/dish_list.html', context)


def category_dishes(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    dishes = Dish.objects.select_related('category', 'cuisine').filter(category=category)
    dishes = apply_filters_and_sorting(request, dishes)

    categories = Category.objects.all().order_by('name')
    cuisines = Cuisine.objects.all().order_by('name')

    context = {
        'category': category,
        'dishes': dishes,
        'categories': categories,
        'cuisines': cuisines,
        'current_filters': request.GET,
        'page_title': f'Категорія: {category.name}',
    }
    return render(request, 'dishes/category_list.html', context)


def dish_detail(request, dish_id):
    dish = get_object_or_404(
        Dish.objects.select_related('category', 'cuisine'),
        id=dish_id
    )

    context = {
        'dish': dish,
        'page_title': dish.name,
    }
    return render(request, 'dishes/dish_detail.html', context)
from django.db import models
from django.utils.safestring import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField(max_length=100, verbose_name="Кухня")

    class Meta:
        verbose_name = "Кухня"
        verbose_name_plural = "Кухні"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Тег")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва страви")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    weight = models.PositiveIntegerField(verbose_name="Вага (г)")
    calories = models.PositiveIntegerField(verbose_name="Калорійність")
    spiciness = models.IntegerField(default=0, verbose_name="Гострота (0-5)")
    is_available = models.BooleanField(default=True, verbose_name="Доступність")
    image = models.ImageField(upload_to='dishes/', verbose_name="Фото страви", blank=True, null=True)

    # Зв'язки
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes', verbose_name="Категорія")
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Кухня")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги/Особливості")

    class Meta:
        verbose_name = "Страва"
        verbose_name_plural = "Страви"

    def __str__(self):
        return self.name

    def get_html_photo(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="70">')
        return "Немає фото"

    get_html_photo.short_description = "Мініатюра"
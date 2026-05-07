from django.test import TestCase
from django.urls import reverse

from menu.models import Dish, Category, Cuisine


class DishPagesTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Супи")
        self.cuisine = Cuisine.objects.create(name="Українська")

        self.dish = Dish.objects.create(
            name="Борщ",
            description="Український борщ",
            price=120.00,
            weight=350,
            calories=250,
            category=self.category,
            cuisine=self.cuisine,
            is_available=True,
            spiciness=2,
        )

    # тест головної сторінки меню
    def test_menu_main_page_opens(self):
        response = self.client.get(reverse("dishes:dish_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Борщ")  # важливо!

    # тест детальної сторінки
    def test_dish_detail_page_opens(self):
        response = self.client.get(
            reverse("dishes:dish_detail", args=[self.dish.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Борщ")
        self.assertContains(response, "Український борщ")
#Тестування моделей страв

from decimal import Decimal
from django.test import TestCase
from .models import Category, Cuisine, Tag, Dish

class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Піца")

        self.assertEqual(category.name, "Піца")

    def test_category_str(self):
        category = Category.objects.create(name="Салати")

        self.assertEqual(str(category), "Салати")


class CuisineModelTest(TestCase):
    def test_cuisine_creation(self):
        cuisine = Cuisine.objects.create(name="Італійська")

        self.assertEqual(cuisine.name, "Італійська")

    def test_cuisine_str(self):
        cuisine = Cuisine.objects.create(name="Українська")

        self.assertEqual(str(cuisine), "Українська")


class TagModelTest(TestCase):
    def test_tag_creation(self):
        tag = Tag.objects.create(name="Гостре")

        self.assertEqual(tag.name, "Гостре")

    def test_tag_str(self):
        tag = Tag.objects.create(name="Вегетаріанське")

        self.assertEqual(str(tag), "Вегетаріанське")


class DishModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Піца")
        self.cuisine = Cuisine.objects.create(name="Італійська")
        self.tag = Tag.objects.create(name="Популярне")

        self.dish = Dish.objects.create(
            name="Маргарита",
            description="Класична піца з томатами та сиром",
            price=Decimal("250.00"),
            weight=500,
            calories=850,
            spiciness=1,
            is_available=True,
            category=self.category,
            cuisine=self.cuisine,
        )

    def test_dish_creation(self):
        self.assertEqual(self.dish.name, "Маргарита")
        self.assertEqual(self.dish.description, "Класична піца з томатами та сиром")
        self.assertEqual(self.dish.price, Decimal("250.00"))
        self.assertEqual(self.dish.weight, 500)
        self.assertEqual(self.dish.calories, 850)
        self.assertEqual(self.dish.spiciness, 1)
        self.assertTrue(self.dish.is_available)

    def test_dish_str(self):
        self.assertEqual(str(self.dish), "Маргарита")

    def test_dish_category_relation(self):
        self.assertEqual(self.dish.category.name, "Піца")
        self.assertIn(self.dish, self.category.dishes.all())

    def test_dish_cuisine_relation(self):
        self.assertEqual(self.dish.cuisine.name, "Італійська")

    def test_dish_tags_relation(self):
        self.dish.tags.add(self.tag)

        self.assertIn(self.tag, self.dish.tags.all())

    def test_dish_without_cuisine(self):
        dish = Dish.objects.create(
            name="Борщ",
            description="Український борщ",
            price=Decimal("120.00"),
            weight=350,
            calories=300,
            category=self.category,
            cuisine=None,
        )

        self.assertIsNone(dish.cuisine)

    def test_dish_default_values(self):
        dish = Dish.objects.create(
            name="Салат",
            description="Овочевий салат",
            price=Decimal("100.00"),
            weight=250,
            calories=150,
            category=self.category,
        )

        self.assertEqual(dish.spiciness, 0)
        self.assertTrue(dish.is_available)

    def test_get_html_photo_without_image(self):
        self.assertEqual(self.dish.get_html_photo(), "Немає фото")
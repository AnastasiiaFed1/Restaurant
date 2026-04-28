from django.test import TestCase, RequestFactory

from menu.models import Dish, Category, Cuisine
from dishes.views import apply_filters_and_sorting


class ApplyFiltersAndSortingTests(TestCase):
    def setUp(self):
        # Підготовка тестових даних перед кожним тестом
        self.factory = RequestFactory()

        self.category_soup = Category.objects.create(name="Супи")
        self.category_dessert = Category.objects.create(name="Десерти")

        self.cuisine_ukrainian = Cuisine.objects.create(name="Українська")
        self.cuisine_italian = Cuisine.objects.create(name="Італійська")

        self.borshch = Dish.objects.create(
            name="Борщ",
            description="Український борщ",
            price=120.00,
            weight=350,
            calories=250,
            category=self.category_soup,
            cuisine=self.cuisine_ukrainian,
            is_available=True,
            spiciness=2,
        )

        self.varenyky = Dish.objects.create(
            name="Вареники",
            description="Вареники з картоплею",
            price=150.00,
            weight=300,
            calories=320,
            category=self.category_soup,
            cuisine=self.cuisine_ukrainian,
            is_available=True,
            spiciness=1,
        )

        self.tiramisu = Dish.objects.create(
            name="Тірамісу",
            description="Італійський десерт",
            price=180.00,
            weight=200,
            calories=450,
            category=self.category_dessert,
            cuisine=self.cuisine_italian,
            is_available=False,
            spiciness=0,
        )

    def get_filtered_dishes(self, params):
        # Допоміжний метод створює GET-запит і запускає функцію фільтрації
        request = self.factory.get("/", data=params)
        queryset = Dish.objects.all()
        return apply_filters_and_sorting(request, queryset)

    # Тест фільтрації за пошуком по назві
    def test_filter_by_search_query(self):
        dishes = self.get_filtered_dishes({"q": "Борщ"})

        self.assertIn(self.borshch, dishes)
        self.assertNotIn(self.varenyky, dishes)
        self.assertNotIn(self.tiramisu, dishes)

    # Тест фільтрації за категорією
    def test_filter_by_category(self):
        dishes = self.get_filtered_dishes({
            "category": str(self.category_dessert.id)
        })

        self.assertIn(self.tiramisu, dishes)
        self.assertNotIn(self.borshch, dishes)
        self.assertNotIn(self.varenyky, dishes)

    # Тест фільтрації за кухнею
    def test_filter_by_cuisine(self):
        dishes = self.get_filtered_dishes({
            "cuisine": str(self.cuisine_italian.id)
        })

        self.assertIn(self.tiramisu, dishes)
        self.assertNotIn(self.borshch, dishes)
        self.assertNotIn(self.varenyky, dishes)

    # Тест фільтрації за мінімальною ціною
    def test_filter_by_min_price(self):
        dishes = self.get_filtered_dishes({
            "min_price": "150"
        })

        self.assertIn(self.varenyky, dishes)
        self.assertIn(self.tiramisu, dishes)
        self.assertNotIn(self.borshch, dishes)

    # Тест фільтрації за максимальною ціною
    def test_filter_by_max_price(self):
        dishes = self.get_filtered_dishes({
            "max_price": "150"
        })

        self.assertIn(self.borshch, dishes)
        self.assertIn(self.varenyky, dishes)
        self.assertNotIn(self.tiramisu, dishes)

    # Тест фільтрації тільки доступних страв
    def test_filter_by_available(self):
        dishes = self.get_filtered_dishes({
            "available": "1"
        })

        self.assertIn(self.borshch, dishes)
        self.assertIn(self.varenyky, dishes)
        self.assertNotIn(self.tiramisu, dishes)

    # Тест фільтрації за рівнем гостроти
    def test_filter_by_spiciness(self):
        dishes = self.get_filtered_dishes({
            "spiciness": "2"
        })

        self.assertIn(self.borshch, dishes)
        self.assertNotIn(self.varenyky, dishes)
        self.assertNotIn(self.tiramisu, dishes)

    # Тест сортування за ціною від меншої до більшої
    def test_sort_by_price_ascending(self):
        dishes = list(self.get_filtered_dishes({
            "sort": "price_asc"
        }))

        self.assertEqual(dishes, [
            self.borshch,
            self.varenyky,
            self.tiramisu,
        ])

    # Тест сортування за ціною від більшої до меншої
    def test_sort_by_price_descending(self):
        dishes = list(self.get_filtered_dishes({
            "sort": "price_desc"
        }))

        self.assertEqual(dishes, [
            self.tiramisu,
            self.varenyky,
            self.borshch,
        ])

    # Тест сортування за назвою від А до Я
    def test_sort_by_name_ascending(self):
        dishes = list(self.get_filtered_dishes({
            "sort": "name_asc"
        }))

        self.assertEqual(dishes, [
            self.borshch,
            self.varenyky,
            self.tiramisu,
        ])

    # Тест сортування за назвою від Я до А
    def test_sort_by_name_descending(self):
        dishes = list(self.get_filtered_dishes({
            "sort": "name_desc"
        }))

        self.assertEqual(dishes, [
            self.tiramisu,
            self.varenyky,
            self.borshch,
        ])

    # Тест сортування за замовчуванням — за назвою
    def test_default_sort_by_name(self):
        dishes = list(self.get_filtered_dishes({}))

        self.assertEqual(dishes, [
            self.borshch,
            self.varenyky,
            self.tiramisu,
        ])

    # Тест: неправильна категорія не повинна ламати фільтрацію
    def test_invalid_category_does_not_break_filtering(self):
        dishes = self.get_filtered_dishes({
            "category": "abc"
        })

        self.assertEqual(dishes.count(), 3)

    # Тест: неправильна кухня не повинна ламати фільтрацію
    def test_invalid_cuisine_does_not_break_filtering(self):
        dishes = self.get_filtered_dishes({
            "cuisine": "abc"
        })

        self.assertEqual(dishes.count(), 3)

    # Тест: неправильна мінімальна ціна не повинна ламати фільтрацію
    def test_invalid_min_price_does_not_break_filtering(self):
        dishes = self.get_filtered_dishes({
            "min_price": "wrong"
        })

        self.assertEqual(dishes.count(), 3)

    # Тест: неправильна максимальна ціна не повинна ламати фільтрацію
    def test_invalid_max_price_does_not_break_filtering(self):
        dishes = self.get_filtered_dishes({
            "max_price": "wrong"
        })

        self.assertEqual(dishes.count(), 3)

    # Тест: неправильна гострота не повинна ламати фільтрацію
    def test_invalid_spiciness_does_not_break_filtering(self):
        dishes = self.get_filtered_dishes({
            "spiciness": "wrong"
        })

        self.assertEqual(dishes.count(), 3)

    # Тест одночасного застосування кількох фільтрів
    def test_combined_filters(self):
        dishes = self.get_filtered_dishes({
            "category": str(self.category_soup.id),
            "available": "1",
            "max_price": "130",
        })

        self.assertIn(self.borshch, dishes)
        self.assertNotIn(self.varenyky, dishes)
        self.assertNotIn(self.tiramisu, dishes)
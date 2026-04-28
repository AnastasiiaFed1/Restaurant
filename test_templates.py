#Тестування шаблону вигляду сторінки

from django.test import TestCase
from django.urls import reverse


class BaseTemplateTests(TestCase):

    def test_page_uses_base_template(self):
        response = self.client.get(reverse("dishes:dish_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")

    def test_page_contains_restaurant_title(self):
        response = self.client.get(reverse("dishes:dish_list"))

        self.assertContains(response, "Ресторан")

    def test_page_contains_bootstrap_css(self):
        response = self.client.get(reverse("dishes:dish_list"))

        self.assertContains(
            response,
            "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        )

    def test_page_contains_bootstrap_js(self):
        response = self.client.get(reverse("dishes:dish_list"))

        self.assertContains(
            response,
            "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
        )

    def test_page_contains_navbar(self):
        response = self.client.get(reverse("dishes:dish_list"))

        self.assertContains(response, 'class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm mb-4"')

    def test_page_contains_link_to_dish_list(self):
        response = self.client.get(reverse("dishes:dish_list"))

        self.assertContains(response, reverse("dishes:dish_list"))

    def test_page_contains_content_container(self):
        response = self.client.get(reverse("dishes:dish_list"))

        self.assertContains(response, 'class="container pb-4"')
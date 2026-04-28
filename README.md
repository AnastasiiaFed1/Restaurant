# Restaurant

## Опис проєкту

Це вебзастосунок для управління ресторанним меню, реалізований з використанням Django.

Користувач може переглядати список страв, фільтрувати їх за різними параметрами (категорія, кухня, ціна, доступність, гострота) та сортувати результати.

Проєкт також включає:
- тестування (моделі, шаблони, фільтрація)
- Docker для контейнеризації
- GitHub Actions для CI (автоматичний запуск тестів)

---

## Основні можливості

* Перегляд списку страв
* Фільтрація за:
  - назвою
  - категорією
  - кухнею
  - ціною (мін/макс)
  - доступністю
  - гостротою
* Сортування:
  - за ціною
  - за назвою
* Перегляд деталей страви
* Інтерфейс на Bootstrap
* Повне тестування логіки
* Docker-запуск
* CI через GitHub Actions

---

## Структура проєкту
```
RESTAURANT/
│
├── .github/
│ └── workflows/
│ └── django-ci.yml 
│
├── core/ 
│ ├── __init__.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── dishes/ 
│ ├── __init__.py
│ ├── views.py
│ ├── urls.py
│ ├── test_filters.py 
│ ├── templates/
│ │ ├── base.html
│ │ └── dishes/
│ │ └── dish_list.html
│
├── menu/ 
│ ├── migrations/
│ ├── __init__.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── tests.py 
│ ├── urls.py
│ └── views.py
│
├── media/ 
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── README.md
├── test_templates.py 
└── db.sqlite3
```
---

## Встановлення та запуск

### 1. Клонувати репозиторій
```bash
git clone <your-repo-url>
cd Restaurant
```

### 2. Створити віртуальне середовище
```bash
python -m venv venv
```
Windows:
```bash
venv\Scripts\activate
```

### 3. Встановити залежності
```bash
pip install -r requirements.txt
```

### 4. Виконати міграції
```bash
python manage.py migrate
```

### 5. Запустити сервер
```bash
python manage.py runserver
```

Відкрити:
```
http://127.0.0.1:8000/
```
---

## Запуск через Docker

### Збірка образу
```bash
docker build -t restaurant-app .
```

### Запуск контейнера
```bash
docker run -p 8000:8000 restaurant-app
```

Або через docker-compose:
```bash
docker compose up --build
```
---

## Запуск тестів

### Усі тести
```bash
python manage.py test
```

### Детальний режим
```bash
python manage.py test -v 2
```
---

## GitHub Actions CI

Файл workflow:
```
.github/workflows/django-ci.yml
```

CI автоматично запускається при:

* push у main/master
* pull request

### Що робить CI:

1. Збирає Docker-образ
2. Запускає контейнер
3. Виконує Django-тести всередині контейнера
4. Зупиняє контейнер

Це гарантує, що:

* проєкт збирається
* контейнер працює
* всі тести проходять

---

## Особливості реалізації

* Використано Django ORM
* Реалізована функція фільтрації apply_filters_and_sorting
* Обробка помилок через try/except
* Повне тестування:
    * моделі
    * шаблони
    * фільтрація
* Docker для ізольованого середовища
* GitHub Actions для автоматизації

---

## Автор

Проєкт виконаний в рамках навчального завдання з програмування студентками Федорченко Анастасія, Конопляник Діана, Бачуріна Ольга та Дяденко Катерина.
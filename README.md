# Документация: Stripe для интеграции платежной системы в Django

Эта документация описывает процесс создания интеграции Stripe для приема онлайн-платежей в проекте Django.

## Требования

1. **Stripe аккаунт** — зарегистрируйтесь на [Stripe](https://stripe.com/) и получите **API-ключи**.
2. **Django проект** — убедитесь, что у вас уже есть работающий проект Django.

## Шаг 1: Установка зависимостей

Для работы со Stripe установите необходимые библиотеки:

```bash
pip install stripe django-environ
```

- `stripe` — библиотека для интеграции с API Stripe.
- `django-environ` — для безопасного хранения ключей API.

## Шаг 2: Настройка API-ключей Stripe

Создайте файл `.env` в корневой папке проекта Django и добавьте свои Stripe ключи:

```plaintext
STRIPE_PUBLISHABLE_KEY=ваш_publishable_key
STRIPE_SECRET_KEY=ваш_secret_key
```

Добавьте `.env` в `.gitignore`, чтобы защитить данные от случайной загрузки на публичный репозиторий.

### Настройки в `settings.py`

В `settings.py` загрузите ключи из файла `.env`:

```python
import environ

env = environ.Env()
environ.Env.read_env()

STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
```

## Шаг 3: Создание модели `Product`

Модель `Product` будет хранить данные о товарах, которые можно оплатить через Stripe.

```python
from django.db import models

class Product(models.Model):
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    currency = models.CharField(max_length=10, default="usd")
    amount = models.PositiveIntegerField(help_text="Цена в центах, например, 2000 для $20.00")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

### Миграции базы данных

Создайте и примените миграции для модели `Product`:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Шаг 4: Создание функций для работы с продуктами Stripe

Создайте функцию в `views.py`, чтобы синхронизировать товары в базе данных Django с продуктами и ценами в Stripe:

```python
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Создание продукта в Stripe
    if not product.stripe_product_id:
        stripe_product = stripe.Product.create(
            name=product.name,
            description=product.description
        )
        product.stripe_product_id = stripe_product.id
    
    # Создание цены в Stripe
    if not product.stripe_price_id:
        stripe_price = stripe.Price.create(
            product=product.stripe_product_id,
            unit_amount=product.amount,
            currency=product.currency,
        )
        product.stripe_price_id = stripe_price.id
    
    # Сохранение ID Stripe
    product.save()
```

## Шаг 5: Отображение продуктов на странице и настройка Stripe Checkout

### Представление для отображения продуктов

Создайте представление `product_list` для отображения всех продуктов:

```python
from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
```

### Представление для создания сессии оплаты

Добавьте представление для создания сессии оплаты через Stripe:

```python
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

def create_checkout_session(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': product.stripe_price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('cancel')),
    )
    return redirect(checkout_session.url)
```

## Шаг 6: Шаблон для отображения продуктов (`product_list.html`)

Создайте шаблон `product_list.html`, который отображает список продуктов и кнопку для оплаты:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Список продуктов</title>
</head>
<body>
    <h1>Список продуктов</h1>
    <ul>
        {% for product in products %}
        <li>
            <h2>{{ product.name }}</h2>
            <p>{{ product.description }}</p>
            <p>Цена: {{ product.amount|floatformat:2 }} {{ product.currency }}</p>
            <form action="{% url 'create_checkout_session' product.id %}" method="POST">
                {% csrf_token %}
                <button type="submit">Оплатить</button>
            </form>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
```

## Шаг 7: Настройка URL

Добавьте маршруты для просмотра списка продуктов и создания сессии оплаты в `urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('create-checkout-session/<int:product_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
```

## Шаг 8: Обработчики успешной и отмененной оплаты

Добавьте представления для обработки успешной и отмененной оплаты:

```python
from django.shortcuts import render

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')
```

## Заключение

Теперь ваша интеграция с Stripe завершена. Вы можете:

1. **Создавать продукты** в Django и синхронизировать их с Stripe.
2. **Отображать список продуктов** и генерировать кнопки для оплаты через Stripe Checkout.
3. **Использовать вебхуки Stripe** для отслеживания успешных и отмененных транзакций (необязательно).

---
Да, конечно. Есть несколько дополнительных параметров, которые Stripe предоставляет для продуктов и платежей, и которые могут быть полезны для сохранения в базе данных, чтобы упростить управление продуктами и анализировать данные о транзакциях. Эти параметры помогут расширить функциональность в будущем и улучшить контроль над продажами и управлением продуктами. Вот некоторые полезные параметры:

---

## Дополнительные параметры, которые можно сохранять в базе данных для продуктов

### 1. **Stripe Product**
   - **`product_id`** — уникальный ID продукта в Stripe (обычно `stripe_product_id`, как указано выше). Это необходимо для связи продукта с Stripe и для идентификации продукта в Stripe API.
   - **`active`** — состояние продукта (включен или отключен в Stripe). Это позволяет временно скрывать или блокировать продукт в системе.
   - **`metadata`** — дополнительное поле для хранения пользовательской информации в формате ключ-значение (например, для внутреннего учета категорий, тегов, или типов продукта).
   - **`created`** — время создания продукта в Stripe. Может быть полезно для анализа, когда продукт был добавлен.
   - **`updated`** — время последнего обновления продукта в Stripe, чтобы отслеживать изменения и синхронизировать данные.

### Пример обновленной модели `Product`:

```python
from django.db import models

class Product(models.Model):
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    currency = models.CharField(max_length=10, default="usd")
    amount = models.PositiveIntegerField(help_text="Цена в центах")
    active = models.BooleanField(default=True)  # Новое поле для статуса продукта
    metadata = models.JSONField(blank=True, null=True)  # Поле для произвольных данных
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления

    def __str__(self):
        return self.name
```

---

## Дополнительные параметры, которые можно сохранять для платежей и сессий оплаты

### 2. **Stripe Session**
   - **`session_id`** — уникальный ID сессии оплаты в Stripe (позволяет отслеживать статус сессии).
   - **`status`** — текущий статус сессии (например, `complete`, `expired`, `open`). Это может быть полезно для определения успешных и неудачных платежей.
   - **`payment_status`** — статус платежа (`paid`, `unpaid`, `no_payment_required`). Это помогает фильтровать успешные транзакции.
   - **`customer_email`** — email покупателя, чтобы получить возможность связываться с клиентом.
   - **`currency`** — валюта платежа (например, USD, EUR).
   - **`amount_total`** — общая сумма транзакции в центах, которая была рассчитана для сессии. Полезно для отчетов и анализа выручки.

### Пример модели `PaymentSession`

```python
class PaymentSession(models.Model):
    stripe_session_id = models.CharField(max_length=255, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_email = models.EmailField(blank=True, null=True)  # Email клиента
    currency = models.CharField(max_length=10, default="usd")
    amount_total = models.PositiveIntegerField()  # Общая сумма платежа
    status = models.CharField(max_length=50, blank=True, null=True)  # Статус сессии
    payment_status = models.CharField(max_length=50, blank=True, null=True)  # Статус платежа
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.stripe_session_id} - {self.status}"
```

---

## Пример использования новых параметров

После создания `PaymentSession` и получения ответа от Stripe, можно сохранять дополнительные параметры, как показано ниже:

```python
def create_checkout_session(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': product.stripe_price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('cancel')),
    )
    
    # Сохранение сессии в базу данных
    PaymentSession.objects.create(
        stripe_session_id=checkout_session.id,
        product=product,
        customer_email=request.user.email if request.user.is_authenticated else None,
        currency=product.currency,
        amount_total=product.amount,
        status=checkout_session.status,
        payment_status=checkout_session.payment_status,
    )
    
    return redirect(checkout_session.url)
```
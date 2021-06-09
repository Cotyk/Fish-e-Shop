from django.db import models
import sys
from PIL import Image

from django.contrib.auth import get_user_model

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from decimal import Decimal

from django.utils import timezone as dj_timezone


User = get_user_model()

app_name = 'fishapp'


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


# class CategoryManager(models.Manager):  # Ми тут за table-level функціоналом
#
#     CATEGORY_NAME_COUNT_NAME = {
#         'Ноутбуки': 'notebook__count',
#         'Смартфони': 'smartphone__count',
#     }
#
#     def get_queryset(self):
#         return super().get_queryset()
#
#     def get_categories_for_left_sidebar(self):
#         # Використаємо анотації, бо category.notebook, category.smartphone - не підходить! ("category.product.count"!?)
#         # (Є ще агрегація)
#         _models = get_models_for_count('notebook', 'smartphone')
#         qs = list(self.get_queryset().annotate(*_models))  # (model.Avg) #!! annotate().values() для перевірки
#         # return [dict(id=c['id'], name=c['name'], slug=c['slug'],
#         # count=c[self.CATEGORY_NAME_COUNT_NAME[c['name']]]) for c in qs]
#         data = [
#             dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
#             for c in qs
#         ]
#         return data


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Назва категорії")
    slug = models.SlugField(unique=True)  # URL endpoint ( /categories/notebooks etc.)

    # sidebar_objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})  # В якості регулярного виразу шукай slug

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class SubCategory(models.Model):

    category = models.ForeignKey('Category', verbose_name='Підкатегорія', on_delete=models.CASCADE)
    sub_name = models.CharField(max_length=255, verbose_name='Назва підкатегорії')
    sub_slug = models.SlugField(unique=True)  # URL endpoint ( /categories/vudilishcha/fiderni etc.)

    # sidebar_objects = CategoryManager()

    def __str__(self):
        return self.sub_name

    def get_absolute_url(self):
        return reverse('subcategory_detail', kwargs={'slug': self.category.slug, 'sub_slag': self.sub_slug})
        # В якості регулярного виразу шукай slug i sub_slag

    class Meta:
        verbose_name = 'Підкатегорія'
        verbose_name_plural = 'Підкатегорії'


class Product(models.Model):

    sub_category = models.ForeignKey('SubCategory', verbose_name='Підкатегорія', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Назва')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Зображення")
    description = models.TextField(verbose_name="Опис", blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Ціна")

    def __str__(self):
        return f'{self.sub_category.category.name}, {self.sub_category.sub_name}: {self.title}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупець', on_delete=models.CASCADE)
    # cart.related_products.all()
    cart = models.ForeignKey('Cart', verbose_name='Кошик', on_delete=models.CASCADE)

    # ЗРУЧНО! Для характеристик.
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # мікрофреймворк, який бачить всі моделі
    # object_id = models.PositiveIntegerField()  # ідентифікатор інстанса цієї моделі
    # content_object = GenericForeignKey('content_type', 'object_id')
    product = models.ForeignKey('Product', verbose_name='Продукт', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Загальна ціна')

    def __str__(self):
        return f'Продукт: {self.product.title} (для кошика)'

    def save(self, *args, **kwargs):
        self.final_price = Decimal(self.qty) * self.product.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт (для кошика)'
        verbose_name_plural = 'Продукти (для кошика)'
        ordering = ['product']


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Власник', on_delete=models.CASCADE)
    products = models.ManyToManyField('CartProduct', blank=True, related_name='related_cart')  # products.related_cart
    total_products = models.PositiveIntegerField(default=0)  # Для показу коректної к-сті товарів в кошику
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Загальна ціна')

    # Доповнюємо полями

    # Потрібно, щоб в кошика був признак того, що його тепер ми чіпати не можемо, він належить тому юзеру і він такий то
    for_anonymous_user = models.BooleanField(default=False)  # Кошик вже з товарами і користувач оформив замовлення
    in_order = models.BooleanField(default=False)  # Для неавторизованих (корзина заглушка - положити не може)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Кошик'
        verbose_name_plural = 'Кошики'


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    orders = models.ManyToManyField('Order', related_name='related_customer', verbose_name='Замовлення покупця')

    def __str__(self):
        return f"Покупець: {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Покупець'
        verbose_name_plural = 'Покупці'


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'  # самовивіз
    BUYING_TYPE_DELIVERY = 'delivery'

    # Стан замовлення
    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення в обробці'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовлення виконано'),
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовивіз'),
        (BUYING_TYPE_DELIVERY, 'Доставка'),
    )

    # Замітка: має бути first_name, last_name (типу того), бо може бути оформлено замовником який є в нашій системі,
    # но замовляє він для іншої людини !
    customer = models.ForeignKey(
        'Customer',
        verbose_name='Замовник',
        related_name='related_orders',  # "clashes" error !
        on_delete=models.CASCADE
    )

    first_name = models.CharField(max_length=255, verbose_name='Ім\'я')
    last_name = models.CharField(max_length=255, verbose_name='Прізвище')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    # Треба створити кошик, якому замовлення належить !!!                            то не зовсім правильно!
    cart = models.ForeignKey('Cart', verbose_name='Кошик', on_delete=models.CASCADE, null=True, blank=True)  # !!!!!!!

    address = models.CharField(max_length=1024, verbose_name='Адрес доставки', null=True, blank=True) # самовивіз, т.д.
    status = models.CharField(
        max_length=100,
        verbose_name='Статус',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип замовлення',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Коментар', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення') # користувач не буде бачити
    order_date = models.DateField(verbose_name='Дата отримання замовлення', default=dj_timezone.now())

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

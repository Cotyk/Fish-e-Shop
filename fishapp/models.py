import os
from math import ceil

from django.db import models
# import sys
# from PIL import Image

from django.contrib.auth import get_user_model

# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from decimal import Decimal

from django.utils import timezone
from django.utils.safestring import mark_safe

User = get_user_model()

app_name = 'fishapp'


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


class CategoryManager(models.Manager):  # Ми тут за table-level функціоналом

    # CATEGORY_NAME_COUNT_NAME = {
    #     'Valentyn': 'product__count',
    #     'TTTT': 'product__count',
    #     'EEEE': 'product__count',
    #     'Вудилища': 'product__count'
    # }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        # Використаємо анотації, бо category.notebook, category.smartphone - не підходить! ("category.product.count"?)
        # (Є ще агрегація)
        _models = get_models_for_count('product')
        qs = self.get_queryset().annotate(*_models)  # (model.Avg) #!! annotate().values() для перевірки
        # print(qs[0].values())
        # return [dict(id=c['id'], name=c['name'], slug=c['slug'],
        # count=c[self.CATEGORY_NAME_COUNT_NAME[c['name']]]) for c in qs]
        try:
            # data = [
            #     dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, 'product__count'))
            #     for c in qs
            # ]
            return qs
        except AttributeError as e:
            # data = [
            #     dict(name=c.sub_name, count=getattr(c, 'product__count'))
            #     for c in qs
            # ]
            return qs


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Назва категорії", unique=True)
    slug = models.SlugField(verbose_name="Слаг", unique=True)  # URL endpoint ( /categories/notebooks etc.)
    image = models.ImageField(verbose_name='Зображення', blank=True, null=True)

    objects = models.Manager()
    annotate_objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})  # В якості регулярного виразу шукай slug

    def get_image(self):
        if not self.image:
            return f"{reverse('homepage')}media/assets/no-camera--v1.png"
        return self.image.url

    # method to create a fake table field in read only mode
    def image_tag(self):
        return mark_safe('<img src="%s" width="auto" height="100" />' % self.get_image())

    image_tag.short_description = 'Image'

    class Meta:
        ordering = ['name']
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class SubCategory(models.Model):

    category = models.ForeignKey('Category', verbose_name='Категорія', on_delete=models.PROTECT)
    sub_name = models.CharField(max_length=255, verbose_name='Назва підкатегорії', unique=True)
    sub_slug = models.SlugField(unique=True, verbose_name='Слаг')  # URL endpoint ( /categories/vudilishcha/fiderni etc)
    sub_image = models.ImageField(verbose_name='Зображення', blank=True, null=True)

    objects = models.Manager()
    annotate_objects = CategoryManager()

    def __str__(self):
        return self.sub_name

    # def get_absolute_url(self):
    #     return reverse('catalog', kwargs={'slug': self.category.slug,
    #                                       'sub_slag': self.sub_slug})
    # В якості регулярного виразу шукай slug i sub_slag
    # Here I return the avatar or picture with an owl, if the avatar is not selected

    def get_image(self):
        if not self.sub_image:
            return f"{reverse('homepage')}media/assets/no-camera--v1.png"
        return self.sub_image.url

    # method to create a fake table field in read only mode
    def image_tag(self):
        return mark_safe('<img src="%s" width="auto" height="55" />' % self.get_image())

    image_tag.short_description = 'Image'

    class Meta:
        ordering = ['sub_name']
        verbose_name = 'Підкатегорія'
        verbose_name_plural = 'Підкатегорії'


class Product(models.Model):

    category = models.ForeignKey('Category', verbose_name='Категорія', on_delete=models.PROTECT)
    sub_category = models.ForeignKey(
        'SubCategory', verbose_name='Підкатегорія', on_delete=models.PROTECT, blank=True, null=True
    )

    title = models.CharField(max_length=255, verbose_name='Назва', unique=False)
    code = models.CharField(max_length=50, verbose_name='Артикул', unique=True)
    code_efish = models.CharField(max_length=50, verbose_name='Оригінальний артикул', unique=True)

    # image = models.ImageField(verbose_name="Зображення", blank=True, null=True)
    # images = models.ForeignKey('Images', verbose_name='Фото', null=True, blank=True, related_name='related_product',
    #                            on_delete=models.DO_NOTHING)

    description = models.TextField(verbose_name="Опис", blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Ціна")
    discount = models.IntegerField(verbose_name="Знижка", blank=True, null=True)

    # For calculations
    remaining = models.CharField(max_length=255, verbose_name='Залишок на складі', blank=True, null=True)
    sold = models.PositiveIntegerField(default=0, verbose_name='Продано')

    # Date
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    from_energofish_yes_no = models.CharField(max_length=3, verbose_name='Від Energofish (yes/no)', default='no')
    usd_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Ціна USD', blank=True, null=True)
    uah_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Ціна ГРН', blank=True, null=True)

    def calc_no_discount_price(self):
        if self.discount:
            return Decimal(round(self.price * 100 / (100 - self.discount), 2))

    def calc_discount_price(self):
        if self.discount:
            return Decimal(round(self.price * (100 - self.discount) / 100, 2))

    def calc_5_discount_price(self):
        if self.discount:
            return Decimal(round(self.price * (100 - 5) / 100, 2))

    def calc_10_discount_price(self):
        if self.discount:
            return Decimal(round(self.price * (100 - 10) / 100, 2))

    def calc_usd_discount_price(self):
        if self.discount:
            return Decimal(round(self.usd_price * (100 - self.discount) / 100, 2))

    def calc_uah_discount_price(self):
        if self.discount:
            return Decimal(round(self.uah_price * (100 - self.discount) / 100, 2))

    def __str__(self):
        if self.sub_category:
            return f'{self.sub_category.category.name}; {self.sub_category.sub_name}: {self.title}'
        else:
            return f'{self.category.name}: {self.title}'

    def get_absolute_url(self):
        if self.sub_category:
            return reverse('product', args=[self.category.slug, self.sub_category.sub_slug, self.pk])
        else:
            return reverse('product', args=[self.category.slug, self.pk])

    def get_absolute_add_to_cart(self):
        if self.sub_category:
            return reverse('add_to_cart', args=[self.category.slug, self.sub_category.sub_slug, self.pk])
        else:
            return reverse('add_to_cart', args=[self.category.slug, self.pk])

    def get_absolute_remove_from_cart(self):
        if self.sub_category:
            return reverse('remove_from_cart', args=[self.category.slug, self.sub_category.sub_slug, self.pk])
        else:
            return reverse('remove_from_cart', args=[self.category.slug, self.pk])

    def get_absolute_change_qty(self):
        return reverse('change_qty', args=[self.pk])

    def image_tags(self):
        html = ''

        for image in self.related_images.all():
            html += f"""<img src="{image}" width="55" height="55" /> """

        if not html:
            html = f"""<img src="{reverse('homepage')}media/assets/no-camera--v1.png" width="45" height="45" />"""

        return mark_safe(html)

    image_tags.short_description = 'Image'

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'


class Images(models.Model):

    product = models.ForeignKey('Product', default=None, related_name='related_images', on_delete=models.CASCADE)

    def upload(self, instance):
        prod = Product.objects.filter(id=int(self.product.id)).first()
        if prod.related_images.all().count() > 0:

            collection = []
            for one_image in prod.related_images.all():
                try:
                    collection.append(int(str(one_image)[str(one_image).rfind('_')+1:str(one_image).rfind('.')]))
                except Exception: pass
            # print(collection)

            return f'{prod.code}_{max(collection)+1}.png'

        else:
            return f'{prod.code}_0.png'

    image = models.ImageField(blank=True, upload_to=upload)

    def save(self, *args, **kwargs):
        # try:
        this = Images.objects.filter(image=self.image).first()

        if this:
            this.image.delete()
            os.remove(this.image.path)
        # except: pass
        super(Images, self).save(*args, **kwargs)

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупець', on_delete=models.CASCADE)
    # cart.related_products.all()
    cart = models.ForeignKey('Cart', verbose_name='Кошик', related_name='related_products', on_delete=models.CASCADE)

    # ЗРУЧНО для характеристик.
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # мікрофреймворк, який бачить всі моделі
    # object_id = models.PositiveIntegerField()  # ідентифікатор інстанса цієї моделі
    # content_object = GenericForeignKey('content_type', 'object_id')
    product = models.ForeignKey('Product', verbose_name='Продукт', on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1, verbose_name='Кількість')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, verbose_name='Загальна ціна')

    def __str__(self):
        return f'Продукт: {self.product.title} (для кошика)'

    def save(self, *args, **kwargs):
        self.final_price = Decimal(self.qty) * self.product.price
        super().save(*args, **kwargs)

    def calculate_max_qty(self):
        if self.product.remaining:
            try:
                remaining = int(self.product.remaining)
            except ValueError:
                remaining = 50

            return remaining
        else:
            return None

    class Meta:
        verbose_name = 'Продукт (для кошика)'
        verbose_name_plural = 'Продукти (для кошика)'
        ordering = ['product']


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Власник', on_delete=models.CASCADE)
    products = models.ManyToManyField('CartProduct', blank=True, related_name='related_cart')  # products.related_cart
    total_products = models.PositiveIntegerField(default=0, verbose_name='Всього товарів')  # Для показу коректної к-сті товарів в кошику
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Загальна ціна')

    # Доповнюємо полями

    # Потрібно, щоб в кошика був признак того, що його тепер ми чіпати не можемо, він належить тому юзеру і він такий то
    for_anonymous_user = models.BooleanField(default=False, verbose_name='Для аноніма')  # Кошик вже з товарами і користувач оформив замовлення
    in_order = models.BooleanField(default=False, verbose_name='У замовленні')  # Для неавторизованих (корзина заглушка - покласти товари не може)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Кошик'
        verbose_name_plural = 'Кошики'


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField(
        'Order', related_name='related_customer', verbose_name='Замовлення покупця', blank=True
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

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
    # BUYING_TYPE_COURIER = 'courier'

    PAYMENT_TYPE_AFTER = 'after'
    PAYMENT_TYPE_TRANSACTION = 'transaction'

    # Стан замовлення
    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення в обробці'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовлення виконано'),
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовивіз'),
        (BUYING_TYPE_DELIVERY, 'У відділення'),
        # (BUYING_TYPE_COURIER, 'Кур\'єром'),
    )

    PAYING_CHOICES = (
        (PAYMENT_TYPE_AFTER, 'Післяоплата'),
        (PAYMENT_TYPE_TRANSACTION, 'Переказ'),
    )

    # Замітка: має бути first_name, last_name (типу того), бо може бути оформлено замовником який є в нашій системі,
    # но замовляє він для іншої людини !

    # ORDER
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
    region = models.CharField(max_length=500, verbose_name='Область')
    location = models.CharField(max_length=500, verbose_name='Населений пункт')  # самовивіз, т.д.
    section = models.CharField(max_length=500, verbose_name='Відділення Нової Пошти', null=True, blank=True)
    address = models.CharField(max_length=500, verbose_name='Адреса')
    # street =
    # house_number =
    # flat =
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
    paying_type = models.CharField(
        max_length=100,
        verbose_name='Спосіб оплати',
        choices=PAYING_CHOICES,
        default=PAYMENT_TYPE_AFTER
    )
    comment = models.TextField(verbose_name='Коментар', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення')  # користувач не буде бачити
    # order_date = models.DateField(verbose_name='Дата отримання замовлення', default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

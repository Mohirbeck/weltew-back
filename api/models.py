from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.


class ProductModel(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Название", null=True, blank=True
    )
    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Цена",
        default=0,
        help_text="Цена в рублях",
    )
    discount = models.FloatField(
        default=0, verbose_name="Скидка", null=True, blank=True
    )
    description = RichTextField(null=True, blank=True, verbose_name="Описание")
    is_aktsiya = models.BooleanField(default=False, verbose_name="Акция")
    width = models.CharField(
        max_length=255, verbose_name="Ширина", null=True, blank=True
    )
    height = models.CharField(
        max_length=255, verbose_name="Высота", null=True, blank=True
    )
    length = models.CharField(
        max_length=255, verbose_name="Длина", null=True, blank=True
    )
    colors = models.ManyToManyField(
        "ColorModel", verbose_name="Цвет", related_name="product_color", blank=True
    )
    manufacturer = models.ForeignKey(
        "ManufacturerModel",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Производитель",
        related_name="product_manufacturer",
    )
    material = models.CharField(
        max_length=255, default="", verbose_name="Материал", null=True, blank=True
    )
    availibility = models.BooleanField(default=True, verbose_name="Наличие")
    code = models.CharField(
        max_length=255, default="", verbose_name="Артикуль", null=True, blank=True
    )
    category = models.ForeignKey(
        "ProductCategoryModel",
        on_delete=models.DO_NOTHING,
        default=None,
        null=True,
        blank=True,
        verbose_name="Категория",
        related_name="product_category",
    )
    assembly = models.FileField(
        upload_to="assembly/", default="", verbose_name="Сборка", null=True, blank=True
    )
    youtube_video_id = models.CharField(max_length=255, default="", null=True, blank=True, verbose_name="ID Youtube видео")
    features = models.JSONField(null=True, blank=True, verbose_name="Характеристики")
    url = models.CharField(max_length=255, verbose_name="Ссылка", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    sklad_cat = models.CharField(
        max_length=255,
        default="",
        verbose_name="Категория склада",
        null=True,
        blank=True,
    )
    sklad_cat_2 = models.CharField(
        max_length=255,
        default="",
        verbose_name="Категория склада 2",
        null=True,
        blank=True,
    )
    sklad_collection = models.CharField(
        max_length=255,
        default="",
        verbose_name="Коллекция склада",
        null=True,
        blank=True,
    )

    @property
    def lname(self):
        return self.name.lower()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}"


class Product3DModel(models.Model):
    poster = models.ImageField(upload_to="images/", null=True, blank=True)
    product = models.ForeignKey(
        "ProductModel",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Продукт",
        related_name="product_3d",
    )
    obj = models.FileField(upload_to="3d/", null=True, blank=True)
    url = models.CharField(max_length=255, default="")

    class Meta:
        verbose_name = "3D модель"
        verbose_name_plural = "3D модели"

    def __str__(self):
        return self.url


class ProductCategoryModel(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(
        upload_to="images/", null=True, blank=True, verbose_name="Изображение"
    )
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активность")

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return self.name


class CollectionCategoryModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    image = models.FileField(
        upload_to="images/", null=True, blank=True, verbose_name="Изображение"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    url = models.CharField(max_length=255, default="")

    class Meta:
        verbose_name = "Категория коллекции"
        verbose_name_plural = "Категории коллекций"

    def __str__(self):
        return self.name


class CollectionModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    discount = models.FloatField(
        default=0, verbose_name="Скидка", null=True, blank=True
    )
    description = RichTextField(null=True, blank=True, verbose_name="Описание")
    products = models.ManyToManyField(
        ProductModel, blank=True, related_name="collection", verbose_name="Товары"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    youtube_video_id = models.CharField(max_length=255, default="", null=True, blank=True, verbose_name="ID Youtube видео")
    manufacturer = models.ForeignKey(
        "ManufacturerModel",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Производитель",
        related_name="collection_manufacturer",
    )
    default_products = models.ManyToManyField(
        ProductModel,
        blank=True,
        related_name="default_products",
        verbose_name="Товары по умолчанию",
    )
    url = models.CharField(max_length=255, default="")
    category = models.ForeignKey(
        "CollectionCategoryModel",
        on_delete=models.DO_NOTHING,
        default=None,
        null=True,
        blank=True,
        verbose_name="Категория",
        related_name="collection_category",
    )

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"

    @property
    def lname(self):
        return self.name.lower()

    @property
    def all_images(self):
        return self.images.all()

    def __str__(self):
        return self.name


class CollectionImagesModel(models.Model):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    collection = models.ForeignKey(
        "CollectionModel",
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    url = models.CharField(max_length=255, default="", null=True, blank=True, verbose_name="Ссылка")

    class Meta:
        verbose_name = "Изображение коллекции"
        verbose_name_plural = "Изображения коллекций"

    def __str__(self):
        return self.image.url


class ProductImagesModel(models.Model):
    image = models.ImageField(upload_to="images/")
    product = models.ForeignKey(
        "ProductModel",
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    url = models.CharField(max_length=255, default="", null=True, blank=True, verbose_name="Ссылка")

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    def __str__(self):
        return self.image.url


class ColorModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    color = models.CharField(max_length=7, verbose_name="Цвет")
    image = models.ImageField(
        upload_to="images/", null=True, blank=True, verbose_name="Изображение"
    )
    url = models.CharField(max_length=255, default="", null=True, blank=True, verbose_name="Ссылка")

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def __str__(self):
        return self.name


class ManufacturerModel(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name


class CartModel(models.Model):
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="cart",
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        "ProductModel",
        on_delete=models.CASCADE,
        verbose_name="Товар",
        related_name="cart",
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(verbose_name="Количество", default=1)
    collection = models.ForeignKey(
        "CustomerCollectionModel",
        on_delete=models.CASCADE,
        verbose_name="Коллекция",
        related_name="cart",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"{self.customer}"


class CustomerCollectionModel(models.Model):
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="collections",
        null=True,
        blank=True,
    )
    collection = models.ForeignKey(
        "CollectionModel",
        on_delete=models.CASCADE,
        verbose_name="Товар",
        related_name="customer_collection",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Коллекция пользователя"
        verbose_name_plural = "Коллекции пользователей"

    def __str__(self):
        return f"{self.customer}"


class CustomerCollectionItemModel(models.Model):
    product = models.ForeignKey(
        "ProductModel",
        blank=True,
        related_name="customer_collection_products",
        verbose_name="Товары",
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(verbose_name="Количество", default=1)
    collection = models.ForeignKey(
        "CustomerCollectionModel",
        on_delete=models.CASCADE,
        verbose_name="Коллекция",
        related_name="customer_collection_products",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Коллекция пользователя"
        verbose_name_plural = "Коллекции пользователей"

    def __str__(self):
        return f"{self.product} - {self.quantity} - {self.collection.collection}"



class OrderModel(models.Model):
    fio = models.CharField(max_length=255, verbose_name="ФИО")
    phone = models.CharField(max_length=255, verbose_name="Телефон")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    products = models.TextField(blank=True, null=True, verbose_name="Товары")
    total_price = models.IntegerField(verbose_name="Сумма заказа", default=0)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    lead_id = models.CharField(
        max_length=255, verbose_name="ID сделки", blank=True, null=True
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.fio


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    device = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.name:
            name = self.name
        else:
            name = self.device
        return str(name)


class CurrencyModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(default=11500)

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self):
        return f"{self.name} - {self.value}"


class CRMModel(models.Model):
    secret_key = models.CharField(max_length=255, verbose_name="Секретный ключ")
    integration_id = models.CharField(
        max_length=255, verbose_name="Идентификатор интеграции"
    )
    code_auth = models.TextField(verbose_name="Код авторизации")
    access_token = models.TextField(
        verbose_name="Токен доступа", blank=True, null=True
    )
    refresh_token = models.TextField(
        verbose_name="Токен обновления", blank=True, null=True
    )
    redirect_uri = models.CharField(max_length=255, verbose_name="URI перенаправления")

    class Meta:
        verbose_name = "AmoCRM"
        verbose_name_plural = "AmoCRM"

    def __str__(self):
        return self.integration_id

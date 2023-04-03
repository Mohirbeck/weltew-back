from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from mapbox_location_field.models import LocationField
from django.utils.translation import gettext, gettext_lazy as _

# Create your models here.


class SecondaryBannerModel(models.Model):
    link = models.CharField(verbose_name="Ссылка",
                            max_length=255, default="", null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name="Изображение")
    title = models.CharField(max_length=255, verbose_name="Заголовок", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    def __str__(self):
        return self.link

    class Meta:
        verbose_name = "Второстепенный баннер"
        verbose_name_plural = "Второстепенные баннеры"


class MainBannerModel(models.Model):
    link = models.CharField(verbose_name="Ссылка",
                            max_length=255, default="", null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name="Изображение")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    def __str__(self):
        return self.link

    class Meta:
        verbose_name = "Главный баннер"
        verbose_name_plural = "Главные баннеры"


class PagesModel(models.Model):
    page_name = models.CharField(
        max_length=100,
        default="",
        null=True,
        blank=True,
        verbose_name="Название страницы",
    )
    content = RichTextUploadingField(
        verbose_name="Контент", null=True, blank=True)
    page_id = models.CharField(
        max_length=100, verbose_name="page_id", default="",)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

    def __str__(self):
        return self.page_name


class InstagramTokenModel(models.Model):
    token = models.TextField(verbose_name="Токен")

    class Meta:
        verbose_name = "Instagram Токен"
        verbose_name_plural = "Instagram Токены"

    def __str__(self):
        return self.token


class ContactsModel(models.Model):
    location = LocationField(
        verbose_name="Локация",
        map_attrs={"center": [69.2401, 41.2995], "marker_color": "red"},
        null=True,
        blank=True,
    )
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон номер 1", null=True, blank=True)
    phone_2 = models.CharField(
        max_length=20, verbose_name="Телефон номер 2", null=True, blank=True
    )
    working_hours = models.CharField(
        max_length=100, verbose_name="Рабочие часы", default="Ежедневно, с 11 до 20"
    )
    address = models.CharField(
        max_length=255, verbose_name="Адрес", null=True, blank=True
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.address


class BestSeller(models.Model):
    products = models.ManyToManyField(
        'api.ProductModel', related_name='best_seller', blank=True, verbose_name="Товары")
    collections = models.ManyToManyField(
        'api.CollectionModel', related_name='best_seller', blank=True, verbose_name="Коллекции")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Лидер продаж"
        verbose_name_plural = "Лидер продаж"


class TopRated(models.Model):
    products = models.ManyToManyField(
        'api.ProductModel', related_name='top_rated', blank=True, verbose_name="Товары")
    collections = models.ManyToManyField(
        'api.CollectionModel', related_name='top_rated', blank=True, verbose_name="Коллекции")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Топ продаж"
        verbose_name_plural = "Топ продаж"


class YouTube(models.Model):
    link = models.CharField(max_length=255, verbose_name="Ссылка на видео")
    cover = models.ImageField(upload_to='images/', verbose_name="Обложка")
    title = models.TextField(verbose_name="Заголовок")
    channel_link = models.CharField(
        max_length=255, verbose_name="Ссылка на канал")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "YouTube"
        verbose_name_plural = "YouTube"

    def __str__(self):
        return self.title

class Catalog(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    image = models.ImageField(upload_to='images/', verbose_name="Изображение")
    file = models.FileField(upload_to='files/', verbose_name="Файл")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Каталог"
        verbose_name_plural = "Каталоги"

    def __str__(self):
        return self.title
    
class Tip(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    image = models.ImageField(upload_to='images/', verbose_name="Изображение")
    description = RichTextUploadingField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Совет и идея"
        verbose_name_plural = "Советы и идеи"

    def __str__(self):
        return self.title
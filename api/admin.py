from django.contrib import admin
from flat_json_widget.widgets import FlatJsonWidget
from .models import (
    ProductModel,
    ProductImagesModel,
    ProductCategoryModel,
    CollectionModel,
    CollectionImagesModel,
    CollectionCategoryModel,
    Customer,
    CRMModel,
    OrderModel,
)
from django.contrib.auth.models import User, Group
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.safestring import mark_safe
import requests
import json

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.action(description="Exchanges tokens for a new token")
def new_token(modeladmin, request, queryset):
    for obj in queryset:
        url = "https://saroyconcept.amocrm.ru/oauth2/access_token"
        data = {
            "client_id": obj.integration_id,
            "client_secret": obj.secret_key,
            "grant_type": "authorization_code",
            "code": obj.code_auth,
            "redirect_uri": obj.redirect_uri,
        }
        data = json.dumps(data)
        response = requests.post(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            obj.access_token = response.json()["access_token"]
            obj.refresh_token = response.json()["refresh_token"]
            obj.save()


@admin.action(description="Exchanges refresh token for a new tokens")
def refresh_token(modeladmin, request, queryset):
    for obj in queryset:
        url = "https://saroyconcept.amocrm.ru/oauth2/access_token"
        data = {
            "client_id": obj.integration_id,
            "client_secret": obj.secret_key,
            "grant_type": "refresh_token",
            "refresh_token": obj.refresh_token,
            "redirect_uri": obj.redirect_uri,
        }
        data = json.dumps(data)
        response = requests.post(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            obj.access_token = response.json()["access_token"]
            obj.refresh_token = response.json()["refresh_token"]
            obj.save()


class JsonDocumentForm(forms.ModelForm):
    class Meta:
        widgets = {"features": FlatJsonWidget}


class ProductImageInline(admin.StackedInline):
    model = ProductImagesModel
    extra = 1


class CollectionImageInline(admin.StackedInline):
    model = CollectionImagesModel
    extra = 1


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "img",
        "name",
        "price",
        "discount",
        "code",
        "is_active",
        "availibility",
        "is_aktsiya",
        "category",
    ]
    search_fields = ["name", "price"]
    list_filter = ["category", "is_active", "is_aktsiya"]
    inlines = [ProductImageInline]
    form = JsonDocumentForm
    list_editable = ["price", "discount", "is_active", "is_aktsiya"]

    def img(self, obj):
        if obj.images.all().first():
            return mark_safe(
                f"<img src='{obj.images.all().first().image.url}' width='50px' />"
            )
        return "Нет фото"

    fieldsets = (
        (
            _("Essentials"),
            {
                "fields": (
                    "name",
                    "price",
                    "discount",
                    "is_active",
                    "is_aktsiya",
                    "sklad_cat",
                )
            },
        ),
        (_("Manufacturer"), {"fields": ("manufacturer", "category")}),
        (
            _("Product"),
            {
                "fields": (
                    "code",
                    "material",
                    "colors",
                    "availibility",
                    "youtube_video_id",
                    "url",
                    "description",
                )
            },
        ),
        (
            _("Size"),
            {
                "fields": (
                    "width",
                    "length",
                    "height",
                )
            },
        ),
        (None, {"fields": ("features",)}),
    )

    list_display_links = ["name", "img"]


@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "get_image"]
    
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50"')
        return "Нет фото"


@admin.register(CollectionCategoryModel)
class CollectionCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "image"]
    list_editable = ["image"]


@admin.register(CollectionModel)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["img", "name", "discount", "category", "url"]
    list_display_links = ["name", "img"]
    search_fields = ["name", "category"]
    inlines = [CollectionImageInline]

    fieldsets = (
        ("Общее", {"fields": ("name", "discount", "description", "category", "youtube_video_id", "is_active")}),
        ("Товары", {"fields": ("products", "default_products")}),
    )

    def img(self, obj):
        if obj.images.all().first():
            return mark_safe(
                f"<img src='{obj.images.all().first().image.url}' width='50px' />"
            )
        return "Нет фото"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "device"]


@admin.register(CRMModel)
class CRMAdmin(admin.ModelAdmin):
    list_display = ["integration_id", "secret_key"]
    actions = [refresh_token, new_token]

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['fio', 'phone', 'total_price']
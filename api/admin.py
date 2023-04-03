from django.contrib import admin
from flat_json_widget.widgets import FlatJsonWidget
from .models import ProductModel, ProductImagesModel, ProductCategoryModel, CollectionModel, CollectionImagesModel, CollectionCategoryModel, Customer
from django.contrib.auth.models import User, Group
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.safestring import mark_safe

admin.site.unregister(User)
admin.site.unregister(Group)


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
    list_display = ["img", "name", "price", "discount",
                    "code", "is_active", "availibility", "is_aktsiya", 'category']
    search_fields = ["name", "price"]
    inlines = [ProductImageInline]
    form = JsonDocumentForm
    list_editable = ["price", "discount", "is_active", "is_aktsiya"]

    def img(self, obj):
        if obj.images.all().first():
            return mark_safe(f"<img src='{obj.images.all().first().image.url}' width='50px' />")
        return 'Нет фото'
    fieldsets = (
        (_("Essentials"), {"fields": ("name", "price",
         "discount", "is_active", "is_aktsiya", "sklad_cat",)}),
        (_("Manufacturer"), {"fields": ("manufacturer", "category")}),
        (
            _("Product"),
            {
                "fields": (
                    "code",
                    "material",
                    "colors",
                    "availibility",
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
    list_display = ["name", "parent", 'image']
    list_editable = ["parent", 'image']


@admin.register(CollectionCategoryModel)
class CollectionCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", 'image']
    list_editable = ['image']


@admin.register(CollectionModel)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["img", "name", "discount", "category", 'url']
    list_display_links = ["name", "img"]
    search_fields = ["name", "category"]
    inlines = [CollectionImageInline]

    fieldsets = (
        ("Общее", {"fields": ("name", "discount", "description", "category")}),
        ("Товары", {"fields": ("products", "default_products")}),
    )

    def img(self, obj):
        if obj.images.all().first():
            return mark_safe(f"<img src='{obj.images.all().first().image.url}' width='50px' />")
        return 'Нет фото'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "device"]
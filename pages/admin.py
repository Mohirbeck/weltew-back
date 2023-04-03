from django.contrib import admin
from pages.models import (
    BestSeller,
    TopRated,
    YouTube,
    ContactsModel,
    PagesModel,
    MainBannerModel,
    SecondaryBannerModel,
    InstagramTokenModel,
    Catalog,
    Tip,
)
from django.utils.safestring import mark_safe

# Register your models here.


@admin.register(BestSeller)
class BestSellerAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(TopRated)
class TopRatedAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(YouTube)
class YouTubeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "link",
    )


@admin.register(ContactsModel)
class ContactsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone",
        "email",
        "address",
    )


@admin.register(PagesModel)
class PagesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "page_name",
    )


@admin.register(MainBannerModel)
class MainBannerAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(SecondaryBannerModel)
class SecondaryBannerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "image",
    )


@admin.register(InstagramTokenModel)
class InstagramTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "token",
    )


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = (
        "img",
        "title",
    )

    list_display_links = (
        "title",
        "img"
    )

    def img(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='75px' />")
        return 'Нет фото'


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )

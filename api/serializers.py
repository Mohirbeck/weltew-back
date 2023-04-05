from api.models import (
    ProductCategoryModel,
    ProductModel,
    ProductImagesModel,
    CollectionModel,
    CollectionImagesModel,
    CollectionCategoryModel,
    Customer,
    CartModel,
)
from rest_framework import serializers
from pages.models import (
    BestSeller,
    Catalog,
    TopRated,
    YouTube,
    ContactsModel,
    PagesModel,
    MainBannerModel,
    SecondaryBannerModel,
    InstagramTokenModel,
)


class CollectionImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionImagesModel
        fields = ["image", "id"]


class CollectionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionCategoryModel
        fields = ["name", "id", "image"]


class CollectionSerializer(serializers.ModelSerializer):
    images = CollectionImagesSerializer(many=True, read_only=True)
    category = CollectionCategorySerializer(many=False, read_only=True)

    class Meta:
        model = CollectionModel
        fields = ["name", "id", "images", "category"]


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImagesModel
        fields = ["image", "id"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source="category.name", read_only=True, allow_null=True
    )
    price = serializers.SerializerMethodField()
    discount = serializers.IntegerField(read_only=True)
    images = ProductImagesSerializer(many=True, read_only=True)
    collection = CollectionSerializer(
        many=False, read_only=True, source="collection.all.first"
    )

    class Meta:
        model = ProductModel
        exclude = ["url"]

    def get_price(self, obj):
        return f"{obj.price:,.0f}".replace(",", " ")

    def get_collection_name(self, obj):
        collection = obj.collection.all().first()
        if collection:
            return collection.name
        return None


class CollectionRetrieveSerializer(serializers.ModelSerializer):
    images = CollectionImagesSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    default_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = CollectionModel
        fields = "__all__"


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryModel
        fields = "__all__"


class BestSellerSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    collections = CollectionSerializer(many=True, read_only=True)

    class Meta:
        model = BestSeller
        fields = "__all__"
        depth = 1


class TopRatedSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    collections = CollectionSerializer(many=True, read_only=True)

    class Meta:
        model = TopRated
        fields = "__all__"
        depth = 1


class YouTubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTube
        fields = "__all__"


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactsModel
        fields = "__all__"


class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagesModel
        fields = "__all__"


class MainBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainBannerModel
        fields = "__all__"


class SecondaryBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryBannerModel
        fields = "__all__"


class InstagramTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramTokenModel
        fields = "__all__"



class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = "__all__"



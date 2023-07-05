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
    Tip
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

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryModel
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=False, read_only=True)
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
    complementaries = CollectionSerializer(many=True, read_only=True)
    default_products = ProductSerializer(many=True, read_only=True)
    category = CollectionCategorySerializer(many=False, read_only=True)

    class Meta:
        model = CollectionModel
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


class SearchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    category = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    collection = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.images.first():
            return obj.images.first().image.url
        return None

    def get_category(self, obj):
        return obj.category.name

    def get_collection(self, obj):
        # get model name
        model_name = obj._meta.model_name
        if model_name == "collectionmodel":
            return True
        return False


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = "__all__"
from rest_framework import generics
from .models import (
    CollectionCategoryModel,
    ProductModel,
    ProductCategoryModel,
    CollectionModel,
    Customer,
    CartModel
)
from .serializers import (
    CatalogSerializer,
    ProductSerializer,
    ProductCategorySerializer,
    BestSellerSerializer,
    TopRatedSerializer,
    YouTubeSerializer,
    CollectionCategorySerializer,
    ContactsSerializer,
    PagesSerializer,
    MainBannerSerializer,
    SecondaryBannerSerializer,
    InstagramTokenSerializer,
    CollectionRetrieveSerializer,
    CollectionSerializer,
    CustomerSerializer,
    CartSerializer,
    CartPostSerializer,
)
from .filters import ProductFilter, CollectionFilter, CartFilter
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


class ProductViewSet(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter


class ProductRetrieveViewSet(generics.RetrieveAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer


class SimilarProductsViewSet(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        product = ProductModel.objects.get(id=pk)
        return ProductModel.objects.filter(category=product.category).exclude(
            id=product.id
        )[:5]


class ProductCategoryViewSet(generics.ListAPIView):
    queryset = ProductCategoryModel.objects.all()
    serializer_class = ProductCategorySerializer


class ProductCategoryRetrieveViewSet(generics.RetrieveAPIView):
    queryset = ProductCategoryModel.objects.all()
    serializer_class = ProductCategorySerializer


class CollectionCategoryViewSet(generics.ListAPIView):
    queryset = CollectionCategoryModel.objects.all()
    serializer_class = CollectionCategorySerializer


class CollectionCategoryRetrieveViewSet(generics.RetrieveAPIView):
    queryset = CollectionCategoryModel.objects.all()
    serializer_class = CollectionCategorySerializer


class CollectionViewSet(generics.ListAPIView):
    queryset = CollectionModel.objects.all()
    serializer_class = CollectionSerializer
    filterset_class = CollectionFilter


class CollectionRetrieveViewSet(generics.RetrieveAPIView):
    queryset = CollectionModel.objects.all()
    serializer_class = CollectionRetrieveSerializer


class CollectionSimilarViewSet(generics.ListAPIView):
    queryset = CollectionModel.objects.all()
    serializer_class = CollectionSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        collection = CollectionModel.objects.get(id=pk)
        return CollectionModel.objects.filter(category=collection.category).exclude(
            id=collection.id
        )[:5]


class BestSellerViewSet(generics.ListAPIView):
    queryset = BestSeller.objects.all()
    serializer_class = BestSellerSerializer


class TopRatedViewSet(generics.ListAPIView):
    queryset = TopRated.objects.all()
    serializer_class = TopRatedSerializer


class YouTubeViewSet(generics.ListAPIView):
    queryset = YouTube.objects.all()
    serializer_class = YouTubeSerializer


class ContactsViewSet(generics.ListAPIView):
    queryset = ContactsModel.objects.all()
    serializer_class = ContactsSerializer


class PagesViewSet(generics.ListAPIView):
    queryset = PagesModel.objects.all()
    serializer_class = PagesSerializer


class PagesRetrieveViewSet(generics.RetrieveAPIView):
    queryset = PagesModel.objects.all()
    serializer_class = PagesSerializer
    lookup_field = "page_id"


class MainBannerViewSet(generics.ListAPIView):
    queryset = MainBannerModel.objects.all()
    serializer_class = MainBannerSerializer


class SecondaryBannerViewSet(generics.ListAPIView):
    queryset = SecondaryBannerModel.objects.all()
    serializer_class = SecondaryBannerSerializer


class InstagramTokenViewSet(generics.ListAPIView):
    queryset = InstagramTokenModel.objects.all()
    serializer_class = InstagramTokenSerializer


class CustomerViewSet(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerRetrieveViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CatalogViewSet(generics.ListAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

class CartViewSet(generics.ListAPIView):
    queryset = CartModel.objects.all()
    serializer_class = CartSerializer
    filterset_class = CartFilter

class CartRetrieveViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartModel.objects.all()
    serializer_class = CartPostSerializer

class CartCreateViewSet(generics.CreateAPIView):
    queryset = CartModel.objects.all()
    serializer_class = CartPostSerializer
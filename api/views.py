import json
import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from .models import (
    CRMModel,
    CollectionCategoryModel,
    ProductModel,
    ProductCategoryModel,
    CollectionModel,
    Customer,
    CartModel,
    CustomerCollectionModel,
    OrderModel,
    CustomerCollectionItemModel,
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
    SearchSerializer,
)
from itertools import chain
from .filters import ProductFilter, CollectionFilter
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


class CatalogViewSet(generics.ListAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


def refresh_token():
    queryset = CRMModel.objects.all()
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


class OrderToCRM(APIView):
    def post(self, request, format=None):
        refresh_token()
        url = "https://saroyconcept.amocrm.ru/api/v4/leads/complex"
        headers = {
            "Authorization": f"Bearer {CRMModel.objects.first().access_token}",
            "Content-Type": "application/json",
        }
        data = request.data
        text = ""
        if len(data["collections"]) > 0:
            for collection in data["collections"]:
                coll = CollectionModel.objects.get(id=collection["id"])
                products = [
                    f"{item['name']} - {item['quantity']} шт,"
                    for item in collection["products"]
                ]
                ps = "\n".join(products)
                text += f"Коллекция {collection['name']}:" + "\n" + ps + "\n"
        if len(data["products"]) > 0:
            products = [
                f"{item['name']} - {item['quantity']} шт," for item in data["products"]
            ]
            ps = "\n".join(products)
            text += f"Продукты:" + "\n" + ps + "\n"
        order = OrderModel.objects.create(
            fio=data["name"],
            total_price=data["total"],
            products=text,
            phone=data["phone"],
            comment=data["comment"],
        )
        req_data = [
            {
                "created_by": 0,
                "price": int(order.total_price),
                "custom_fields_values": [
                    {"field_id": 1065243, "values": [{"value": text}]}
                ],
                "pipeline_id": 6664814,
                "_embedded": {
                    "contacts": [
                        {
                            "first_name": order.fio,
                            "custom_fields_values": [
                                {
                                    "field_code": "PHONE",
                                    "values": [{"value": order.phone}],
                                }
                            ],
                        }
                    ]
                },
            }
        ]
        req_data = json.dumps(req_data)
        response = requests.post(url, data=req_data, headers=headers)
        print(req_data)
        if response.status_code == 200:
            order.lead_id = response.json()[0]["id"]
            order.save()

        return Response({"success": True})

    # if collection:
    # products = [
    #     f"{item.product.name} - {item.quantity} шт" for item in order.products.all()
    # ]
    # ps = "\n".join(products)
    # text = f"Коллекции {collection}" + "\n" + ps
    # else:
    #     products = [
    #         f"{item.product.name} - {item.quantity} шт" for item in order.products.all()
    #     ]
    #     text = "\n".join(products)
    # data = [
    #     {
    # "created_by": 0,
    # "price": int(order.total_price),
    # "custom_fields_values": [
    #     {"field_id": 1065243, "values": [{"value": text}]}
    # ],
    # "pipeline_id": 6222090,
    # "_embedded": {
    #     "contacts": [
    #         {
    #             "first_name": order.fio,
    #             "custom_fields_values": [
    #                 {"field_code": "PHONE", "values": [{"value": order.phone}]}
    #             ],
    #         }
    #     ]
    # },
    #     }
    # ]
    # data = json.dumps(data)
    # response = requests.post(url, data=data, headers=headers)
    # if response.status_code == 200:
    #     order.lead_id = response.json()[0]["id"]
    #     order.save()

class Search(APIView, LimitOffsetPagination):
    def get(self, request):
        query = request.GET.get("q", None)
        products = ProductModel.objects.all()
        collections = CollectionModel.objects.all()
        if query:
            print(query)
            products = products.filter(name__icontains=query)
            collections = collections.filter(name__icontains=query)
            print(products, collections)
            # queryset = self.paginate_queryset(queryset, request, view=self)
        queryset = list(chain(collections, products))
        queryset = self.paginate_queryset(queryset, request, view=self)
        serializer = SearchSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)
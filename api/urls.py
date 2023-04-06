from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import api.views as views

schema_view = get_schema_view(
    openapi.Info(
        title="Weltew API",
        default_version='v1',
        description="Api documentation for the Weltew API",
        contact=openapi.Contact(email="mustaqimovmohir@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
    path('products/', views.ProductViewSet.as_view()),
    path('products/<int:pk>/', views.ProductRetrieveViewSet.as_view()),
    path('products/<int:pk>/similar', views.SimilarProductsViewSet.as_view()),
    path('collections/', views.CollectionViewSet.as_view()),
    path('collections/<int:pk>/', views.CollectionRetrieveViewSet.as_view()),
    path('collections/<int:pk>/similar',
         views.CollectionSimilarViewSet.as_view()),
    path('categories/', views.ProductCategoryViewSet.as_view()),
    path('categories/<int:pk>/', views.ProductCategoryRetrieveViewSet.as_view()),
    path('collections/categories/', views.CollectionCategoryViewSet.as_view()),
    path('collections/categories/<int:pk>/', views.CollectionCategoryRetrieveViewSet.as_view()),
    path('banners/main/', views.MainBannerViewSet.as_view()),
    path('banners/secondary/', views.SecondaryBannerViewSet.as_view()),
    path('social/instagram/', views.InstagramTokenViewSet.as_view()),
    path('social/youtube/', views.YouTubeViewSet.as_view()),
    path('pages/', views.PagesViewSet.as_view()),
    path('pages/<str:page_id>/', views.PagesRetrieveViewSet.as_view()),
    path('catalogs/', views.CatalogViewSet.as_view()),
    path('bestsellers/', views.BestSellerViewSet.as_view()),
    path('toprated/', views.TopRatedViewSet.as_view()),
    path('contacts/', views.ContactsViewSet.as_view()),
    path('checkout/', views.OrderToCRM.as_view()),
    path('search/', views.Search.as_view()),
]

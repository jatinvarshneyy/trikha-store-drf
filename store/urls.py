from django.urls import path
from . import views

urlpatterns = [
    # Products Urls
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('product/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),

    # Collection Urls
    path('collections/', views.CollectionList.as_view(), name='collection-list'),
    path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
]
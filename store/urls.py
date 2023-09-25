from django.urls import path
from . import views

urlpatterns = [
    # Products Urls
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('product/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),

    # Collection Urls
    path('collections/', views.collection_list, name='collection-list'),
    path('collection/<int:pk>/', views.collection_detail, name='collection-detail'),
]
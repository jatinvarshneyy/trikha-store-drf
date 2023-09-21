from django.urls import path
from . import views

urlpatterns = [
    # Products Urls
    path('products/', views.product_list, name='product-list'),
    path('product/<int:id>/', views.product_detail, name='product-detail'),

    # Collection Urls
    path('collections/', views.collection_list, name='collection-list'),
    path('collection/<int:pk>/', views.collection_detail, name='collection-detail'),
]
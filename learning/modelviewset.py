"""
----> Using a ModelViewSet saves you from writing repetitive code for CRUD operations and provides a standardized way to interact with your database models through a RESTful API. It simplifies API development and makes your code more organized and maintainable. With ModelViewSet, you don't have to write the same CRUD (Create, Retrieve, Update, Delete) operations code in different views. Instead, you can write all of these operations in a single view, which makes your code cleaner, more organized, and professional. It's like having a one-stop-shop for managing your data through a web API.
"""

# Imports
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.db.models import Count
from store.models import Product, OrderItem, Collection
from store.serializers import ProductSerializer, CollectionSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product Cannot be allowed because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
# CollectionViewSet
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'})
        return super().destroy(request, *args, **kwargs)

    """
    ----> When using a ModelViewSet, there's no need for separate functions to handle CRUD operations; you can perform all these operations within a single view. Plus, if you need to customize any of these operations, like the 'destroy' method for deleting records, you can easily override them within the view. This approach streamlines your code, improves maintainability, and is considered a professional way to handle CRUD operations in a Django REST API. However, to make ModelViewSet work with URLs, you do need to configure routers as using simple URL patterns alone won't work. These routers help map the view to the appropriate URLs, making your API more organized and professional.
    """

# Router Patterns
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)

# UrlConf
urlpatterns = router.urls

"""
----> Using DefaultRouter() with ModelViewSet is a good practice. It not only automatically generates URLs for your API endpoints but also enhances the API's professionalism and usability in several ways:

Browsable API: When you navigate to the home URL, it provides a browsable API interface, which makes it easier to explore and understand the available API endpoints. This is especially useful during development and for API users who are not familiar with the API structure.

Content Negotiation: By appending .json or other format extensions to the URLs, it allows users to explicitly specify the desired response format (e.g., JSON). This adds flexibility and user-friendliness to the API because clients can request data in the format they prefer.

So, using DefaultRouter() not only makes your API more professional but also improves its accessibility and user experience.
"""


# Very first we need to install drf-nested-routers using pip

from . import views
# Then importing routers from rest_framework_nested
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

# First we need to define the parent router with parameter name - router:parent-router, 'products':parent_url, lookup:'product'
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')

# Then we register child viewset url with parent router url
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

# UrlConf
urlpatterns = router.urls + products_router.urls
"""
-> Why We Use Class Based View?

-------> Control and Flexibility <-------
   - Imagine you're making a pizza. With APIView, you get to decide what toppings to put on, how much cheese to use, and how long to bake it. It's like having total control.
   - In coding terms, APIView gives you complete control over what data to send back as a response for each type of request.

-----------> Customization <-------------
   - Just like everyone has their favorite type of pizza, every project has unique requirements. Maybe you want to make sure only certain people can order your pizza, or you want to add special instructions.
   - APIView lets you customize your API endpoints to match your project's specific needs.
   
-----------> Reusable Code <-------------
   - Think of APIView as a recipe. Once you have a great pizza recipe, you can use it over and over to make different pizzas.
   - With APIView, you write the code once and can use it for multiple API endpoints. This makes your code more organized and saves you time.

-> In summary, APIView is like a chef's kitchen where you have control, flexibility, and the ability to customize how you make and serve different types of requests, like making and serving different kinds of pizzas. It makes coding API endpoints easier and more organized.
"""

"""

------------------------------------------> APIView : Starts Here <------------------------------------------------

-----------> This is how we writing the urls patterns for handling the CBV : Starts Here <-------------

from django.urls import path
from . import views

urlpatterns = [
    # Products Urls
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('product/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),
]

-----------> This is how we writing the urls patterns for handling the CBV : Ends Here <---------------

------------------> Imports : APIView : Starts Here <--------

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from store.models import Product
from store.serializers import ProductSerializer

------------------> Imports : APIView : Ends Here <----------


-------> Product List View : APIView : Starts Here <---------
class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

-------> Product List View : APIView : Ends Here <-----------
    

-------> Product Detail View : APIView : Starts Here <-------
class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product Cannot be allowed because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

---------> Product Detail View : APIView : Ends Here <--------

-> In summary, using Class-Based Views provides greater control and flexibility in handling API endpoints, promotes code reusability, results in more concise and elegant code, and enhances the overall professionalism of your code. It allows you to write less code while maintaining code quality and structure.
"""

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from store.models import Product
from store.serializers import ProductSerializer

# Product List : APIView
class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

# Product Detail : APIView
class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product Cannot be allowed because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
------------------------------------------> APIView : Ends Here <------------------------------------------------
"""


"""
-----------------------------> Generic Views : ListCreateAPIView : Starts Here <---------------------------------

------------------> Imports : ListCreateAPIView : Starts Here <--------

from rest_framework.generics import ListCreateAPIView
from store.models import Product
from store.serializers import ProductSerializer

------------------> Imports : ListCreateAPIView : Ends Here <----------


------> Product List View : ListCreateAPIView : Starts Here <----------
-> This method is use when we want override the methods.

class ProductList(ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.select_related('collection').all()
    
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

    -> When we use ListCreateAPIView, we have the option to define individual methods as needed. However, we typically override these methods when customization is required. Otherwise, the Django Rest Framework provides us with default implementations for these methods.In summary, by only overriding the methods that need customization and utilizing the built-in methods for the rest, we maintain professionalism and keep our code clean and efficient. This approach ensures that we make the best use of the framework's tested and reliable functionality.

------> Product List View : ListCreateAPIView : Ends Here <------------


------> Product List View : ListCreateAPIView : Starts Here <----------
-> If we dont want to override the methods then we use directly inbuilt-methods.

class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

------> Product List View : ListCreateAPIView : Ends Here <------------


-> Product Detail View : RetrieveUpdateDestroyAPIView : Starts Here <--
-> This is how we customizing the generic views.

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    
    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product Cannot be allowed because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

-> Product Detail View : RetrieveUpdateDestroyAPIView : Ends Here <----

"""

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from store.models import Product
from store.serializers import ProductSerializer

# Product List : ListCreateAPIView
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
# Product Detail : RetrieveUpdateDestroyAPIView
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    
    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product Cannot be allowed because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
"""
-----------------------------> Generic Views : ListCreateAPIView : Ends Here <-----------------------------------
"""


"""
----------------------------------------> ModelViewSet : Starts Here <-------------------------------------------

-> Using a ModelViewSet saves you from writing repetitive code for CRUD operations and provides a standardized way to interact with your database models through a RESTful API. It simplifies API development and makes your code more organized and maintainable. With ModelViewSet, you don't have to write the same CRUD (Create, Retrieve, Update, Delete) operations code in different views. Instead, you can write all of these operations in a single view, which makes your code cleaner, more organized, and professional. It's like having a one-stop-shop for managing your data through a web API.

------------------> Imports : ModelViewSet : Starts Here <--------

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Product, OrderItem
from .serializers import ProductSerializer

------------------> Imports : ModelViewSet : Ends Here <----------

-------------> Product : ModelViewSet : Starts Here <-------------
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

    
    -> When using a ModelViewSet, there's no need for separate functions to handle CRUD operations; you can perform all these operations within a single view. Plus, if you need to customize any of these operations, like the 'destroy' method for deleting records, you can easily override them within the view. This approach streamlines your code, improves maintainability, and is considered a professional way to handle CRUD operations in a Django REST API. However, to make ModelViewSet work with URLs, you do need to configure routers as using simple URL patterns alone won't work. These routers help map the view to the appropriate URLs, making your API more organized and professional.

    -----------> This is how we writing the Router patterns for handling ModelViewSet : Starts Here <-------------

    from . import views
    from rest_framework.routers import DefaultRouter

    router = DefaultRouter()
    router.register('products', views.ProductViewSet)

    # UrlConf
    urlpatterns = router.urls

    -----------> This is how we writing the Router patterns for handling ModelViewSet : Ends Here <---------------

    -> Using DefaultRouter() with ModelViewSet is a good practice. It not only automatically generates URLs for your API endpoints but also enhances the API's professionalism and usability in several ways:

    Browsable API: When you navigate to the home URL, it provides a browsable API interface, which makes it easier to explore and understand the available API endpoints. This is especially useful during development and for API users who are not familiar with the API structure.

    Content Negotiation: By appending .json or other format extensions to the URLs, it allows users to explicitly specify the desired response format (e.g., JSON). This adds flexibility and user-friendliness to the API because clients can request data in the format they prefer.

    So, using DefaultRouter() not only makes your API more professional but also improves its accessibility and user experience.

-------------> Product : ModelViewSet : Ends Here <---------------
"""

# Routers Patterns for ModelViewSet
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

# UrlConf
urlpatterns = router.urls

# ModelViewSet imports and how we use ModelViewSet
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from store.models import Product, Collection, OrderItem
from store.serializers import ProductSerializer, CollectionSerializer

# ProductViewSet
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
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
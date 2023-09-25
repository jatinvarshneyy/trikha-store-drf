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

------------------------------------------> APIView <--------------------------------------------------

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
-----------------------------> Generic Views : ListCreateAPIView <---------------------------------

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
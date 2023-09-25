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

-> APIView is like a chef's kitchen where you have control, flexibility, and the ability to customize how you make and serve different types of requests, like making and serving different kinds of pizzas. It makes coding API endpoints easier and more organized.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Products Urls
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('product/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),
]

# Imports
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
----> In summary, using Class-Based Views provides greater control and flexibility in handling API endpoints, promotes code reusability, results in more concise and elegant code, and enhances the overall professionalism of your code. It allows you to write less code while maintaining code quality and structure.
"""
"""
------------------> Imports : Function Based Views : Starts Here <------------------

from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerializer

------------------> Imports : Function Based Views : Ends Here <--------------------


------------> Product List View : Function Based Views : Starts Here <--------------
# Product List View
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == "GET":
        # When we wants to GET a list of products - We fetch all products from the database, and also include related collections.
        queryset = Product.objects.select_related('collection').all()
        # We create a serializer to convert this data into a format that can be sent as a response - We pass in the request object so that the serializer knows about the request details - When you have a queryset or a list of objects, you need to specify (many=True) to tell the serializer that you are dealing with multiple objects.
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        # Finally, we send back the serialized data as a response.
        return Response(serializer.data)

    elif request.method == "POST":
        # When someone wants to POST (create) a new product - We create a serializer using the data that they sent in the request.
        serializer = ProductSerializer(data=request.data)
        # Validating Data with django -'exception=True' it automates validate the data and return the specific error for specific validation 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)        
        
        
        -----> Code - Validating the data with if-else block : Starts Here <------
            serializer = ProductSerializer(data=request.data)  
            if serializer.is_valid():
                serializer.validated_data
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        -----> Code - Validating the data with if-else block : Ends Here <--------

------------> Product List View : Function Based Views : Ends Here <--------------


----------> Product Detail View : Function Based Views : Starts Here <------------
# Product Detail View
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    elif request.method == "DELETE":
        if product.orderitems.count() > 0:
            return Response({'error': 'Product Cannot be allowed because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
    - Error Handling and 404 Status Code: get_object_or_404 is a Django shortcut function commonly used to retrieve a single object from the database, and it raises a Http404 exception if the object is not found. This is a convenient way to handle the case where an object does not exist because it automatically triggers the 404 error response, which is a standard way to indicate to clients that the requested resource was not found.
    
 
    
    -----> Code - Validating the data with if-else block : Starts Here <------
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    ------> Code - Validating the data with if-else block : Ends Here <-------

----------> Product Detail View : Function Based Views : Ends Here <------------


--------> Collection List View : Function Based Views : Starts Here <-----------
# Collection List View
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(products_count=Count('products'))
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
---------> Collection List View : Function Based Views : Ends Here <------------


--------> Collection Detail View : Function Based Views : Ends Here <-----------
# Collection Detail View
@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), id=pk)
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    elif request.method == "DELETE":
        if collection.products.count() > 0:
            return Response({'error': 'Collection Cannot be allowed because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
----------> Collection Detail View : Function Based Views : Ends Here <------------
"""

from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerializer

# Product List View
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == "GET":
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)        
        
        """
        - Code - Validating the data with if-else block :

            serializer = ProductSerializer(data=request.data)  
            if serializer.is_valid():
                serializer.validated_data
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """

# Product Detail View
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    elif request.method == "DELETE":
        if product.orderitems.count() > 0:
            return Response({'error': 'Product Cannot be allowed because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
        """
        - Code - Handling the data with try-except block :

            try:
                product = Product.objects.get(id=id)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        """

# Collection List View
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(products_count=Count('products'))
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

# Collection Detail View
@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), id=pk)
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    elif request.method == "DELETE":
        if collection.products.count() > 0:
            return Response({'error': 'Collection Cannot be allowed because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# Product List View
@api_view()
def product_list(request):
    queryset = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

    """ 
    - By using 'context={'request': request}' when initializing your serializer, you're passing in the request object from the view or API endpoint to the serializer. This allows the serializer to access information about the request, such as the user making the request, authentication details, query parameters, and more.

    - The '.select_related('collection')' part of the query tells Django to fetch related data from the collection model in a single query, instead of making separate queries for each related item. This can significantly improve query performance, especially when dealing with a large amount of data, as it reduces the number of database queries needed.

    - When you have a queryset or a list of objects, you need to specify (many=True) to tell the serializer that you are dealing with multiple objects.
    """

# Product Detail View
@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

    """
    - Error Handling and 404 Status Code: get_object_or_404 is a Django shortcut function commonly used to retrieve a single object from the database, and it raises a Http404 exception if the object is not found. This is a convenient way to handle the case where an object does not exist because it automatically triggers the 404 error response, which is a standard way to indicate to clients that the requested resource was not found.
    """
 
    """
    - Code - Handling the data with try-except block :

        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    """

# Collection Detail View
@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, id=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)
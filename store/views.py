from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer

# Product List View
@api_view()
def product_list(request):
    queryset = Product.objects.all()
    """ 
    - When you have a queryset or a list of objects, you need to specify many=True to tell the serializer that you are dealing with multiple objects.
    """
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)

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
    - Handling the data with try-except block :

        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    """
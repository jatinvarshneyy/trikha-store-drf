from rest_framework import serializers
from .models import Product
from decimal import Decimal

# Product Serializer
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)
    
    """
    - 'price_with_tax': This is a custom field you're defining in your serializer. It's not a direct attribute of your model but rather a calculated value that you want to include when serializing an object.

    - 'serializers.SerializerMethodField': This field allows you to define a custom method (calculate_tax in this case) to compute the value of the field. It's particularly useful when you need to perform complex calculations or include data that doesn't directly map to a model attribute.

    - 'calculate_tax' Method: This method calculates the tax-inclusive price for a product. It takes one argument, product, which is assumed to be an instance of the Product model. Inside the method, it multiplies the unit_price of the product by a tax rate of 1.1 (which represents a 10% tax or a 110% total price).
    """
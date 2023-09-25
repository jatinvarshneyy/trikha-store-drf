from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal

# Collection Serializer
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']

    """
    - A Model Serializer in Django REST framework offers code optimization by automatically generating serialization fields based on the structure of a model. It eliminates the need to define each field manually, saving developers time and reducing redundancy. While Model Serializers can automatically include all fields from the model, developers have the flexibility to customize which fields are exposed in the serialized output. This customization ensures that only the necessary data is exposed, enhancing security and performance in API development.
    """

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    """ 
    - source = "unit_price": This indicates that when you serialize this field, you should use the value from the unit_price attribute of the model. In other words, you're telling the serializer to look for the value in the unit_price attribute and use it when serializing the price field.
    """
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax') 
    
    """
    - 'price_with_tax': This is a custom field you're defining in your serializer. It's not a direct attribute of your model but rather a calculated value that you want to include when serializing an object.
    
    - 'serializers.SerializerMethodField': This field allows you to define a custom method (calculate_tax in this case) to compute the value of the field. It's particularly useful when you need to perform complex calculations or include data that doesn't directly map to a model attribute.

    - 'calculate_tax' Function, we are using in 'price_with_tax' custom serializer field.
    """
    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)
    

    """
    - Serializing Relationships :

    1. PrimaryKeyRelatedField: When working with Django models that have foreign key relationships, you can use the PrimaryKeyRelatedField in your serializer to represent these relationships. This field allows you to associate a related object by its primary key (ID). However, it's essential to be aware that when you use PrimaryKeyRelatedField, it returns the primary key (ID) of the related object, rather than its name or title. In this we need to pass an parameter like queryset.
    
    Code:
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )
    ----------------------------------------------------------------------------------------------------------------
    
    2. StringRelatedField: This field returns a string representation of the related object. In the case of a foreign key relationship, it would typically return the human-readable attribute, such as the name or title, of the related object instead of its primary key. 

    Code:
    collection = serializers.StringRelatedField()
    ----------------------------------------------------------------------------------------------------------------

    3. CollectionSerializer: The method called "Nested Object Serialization," involves creating a separate serializer for a related object and using it as a field within another serializer.

    Code:
    collection = CollectionSerializer()
    ----------------------------------------------------------------------------------------------------------------

    4. HyperlinkedRelatedField: This method allows you to create a hyperlink to a specific view for related objects. You provide the reference to the view using the view_name parameter.

    Code:
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail',
    )
    """
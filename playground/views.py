from django.shortcuts import render
from store.models import Product

# Home View Functionality...
def home(request):
    queryset = Product.objects.all() 

    context = {
        'queryset': queryset,
    }
    return render(request, "playground/home.html", context)

# Products View Functionality...
def products(request):
    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, "playground/products.html", context)
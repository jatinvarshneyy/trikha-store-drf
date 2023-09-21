from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Product List View
@api_view()
def product_list(request):
    return Response("Product List View Working Fine")

# Product Detail View
@api_view()
def product_detail(request, id):
    return Response(f"Product Detail View Working Fine - Product ID: {id}")
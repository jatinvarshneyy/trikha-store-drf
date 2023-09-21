from django.contrib import admin
from .models import Tag, TaggedItem

# Registering Tag Model...
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'label',]
    search_fields = ['label']
    list_per_page = 10
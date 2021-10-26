from django.contrib import admin
from .models import Seller_Details,Products,ProductImage,Brand

# Register your models here.
admin.site.register(Seller_Details)
admin.site.register(Brand)
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model = Products

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

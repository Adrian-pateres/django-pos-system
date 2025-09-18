from django.contrib import admin
from .models import Product, Transaction, TransactionItem

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('price',)

class TransactionItemInline(admin.TabularInline):
    model = TransactionItem
    extra = 1

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'teller', 'created_at')
    list_filter = ('created_at', 'teller')
    inlines = [TransactionItemInline]

@admin.register(TransactionItem)
class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'product', 'quantity')
    list_filter = ('product',)
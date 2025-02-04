from django.contrib import admin
from .models import Category, Subcategory, Product, Cart, CartItem, Customer, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1 

# Inline for Order inside Customer
class OrderInline(admin.TabularInline):
    model = Order
    extra = 1  

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('customer__name', 'user__username')
    inlines = [OrderItemInline]  

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'city', 'state')
    search_fields = ('name', 'email', 'mobile')
    inlines = [OrderInline]  

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)

from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Cart, CartItem, Product, Category

def product_view(request):
    products = Product.objects.all().distinct()  

    # Search functionality
    search_query = request.GET.get('search', '').strip()  
    if search_query:
        search_words = search_query.split()
        query = Q()
        for word in search_words:
            query |= Q(name__icontains=word) | Q(description__icontains=word)
        products = products.filter(query).distinct()  

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(subcategory__category_id=category_id).distinct()  

    # Pagination (12 products per page)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all categories for filter dropdown
    categories = Category.objects.all()

    # Define `context` outside of conditions
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
    }

    return render(request, 'product.html', context)


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request,'add to cart successfully')
    return redirect('shop')

def view_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


def increment_item(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    cart_item.increment_quantity()
    messages.success(request,'increment successfully')
    return redirect('view_cart')

def decrement_item(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    cart_item.decrement_quantity()
    messages.success(request,'decrement successfully')
    return redirect('view_cart')

def remove_item(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    cart_item.delete()
    messages.success(request,'remove successfully')
    return redirect('view_cart')

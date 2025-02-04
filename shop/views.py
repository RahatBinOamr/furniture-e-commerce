from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category

def productView(request):
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

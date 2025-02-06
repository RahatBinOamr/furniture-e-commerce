from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from shop.forms import CustomerForm
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Category

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

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    if request.method == 'POST':
        print("Checkout form submitted")  # Debugging print statement
        form = CustomerForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debugging print statement
            customer = form.save(commit=False)
            if request.user.is_authenticated:
                customer.user = request.user  
            customer.save()

            # Retrieve cart items for the user or session
            try:
                if request.user.is_authenticated:
                    cart = get_object_or_404(Cart, user=request.user)
                else:
                    cart = get_object_or_404(Cart, session_key=request.session.session_key)
            except Exception as e:
                print("Error retrieving cart:", e)
                messages.error(request, "Cart not found")
                return redirect('cart_page')

            cart_items = cart.items.all()
            total_price = sum(item.total_price() for item in cart_items)

            # Debugging
            print(f"Total Price: {total_price}")

            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {'name': 'Your Order'},
                                'unit_amount': int(total_price * 100),  # Convert to cents
                            },
                            'quantity': 1,
                        }
                    ],
                    mode='payment',
                    
                    success_url=request.build_absolute_uri(reverse('checkout_success')),
                    cancel_url=request.build_absolute_uri(reverse('checkout_cancel')),
                )
                print("Stripe session created successfully")
                return redirect(checkout_session.url)
            except Exception as e:
                print("Stripe error:", e)
                messages.error(request, "Error processing payment")
                return redirect('checkout_page')

        else:
            print("Form is invalid", form.errors)  # Debugging print statement
            messages.error(request, "Invalid form submission")
            return render_checkout_page(request, form)
    
    return render_checkout_page(request, CustomerForm())



def render_checkout_page(request, form):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
    else:
        cart = get_object_or_404(Cart, session_key=request.session.session_key)
    
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    }
    return render(request, 'checkout.html', context)

def checkout_success(request):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).latest('id')
        cart = get_object_or_404(Cart, user=request.user)
    else:
        customer = Customer.objects.filter(session_key=request.session.session_key).latest('id')
        cart = get_object_or_404(Cart, session_key=request.session.session_key)
    
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)
    messages.success(request,'order checkout successful')
    # Create order
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key if not request.user.is_authenticated else None,
        customer=customer,
        total_price=total_price,
        is_paid=True,
    )

    # Create order items
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price,
        )

    # Clear the cart
    cart.items.all().delete()
    
    context = {
        'order': order,
        'customer': customer,
    }
    return render(request, 'checkout_success.html', context)


def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customer = order.customer
    order_items = order.items.all()

    # Render the invoice HTML
    html_string = render_to_string('invoice_template.html', {
        'order': order,
        'customer': customer,
        'order_items': order_items,
    })
    
    # Generate PDF in memory
    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)

    # Return PDF as a downloadable response
    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'
    
    return response
def checkout_cancel(request):
    return render(request, 'checkout_cancel.html')
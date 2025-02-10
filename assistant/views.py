from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from gtts import gTTS
from shop.models import Product

def assistant(request):
    # Initially, no products are shown
    return render(request, 'assistant/shop.html', {'products': []})

def voice_query(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET.get('query', '').strip().lower()
        
        # Find the closest matching product
        products = Product.objects.filter(name__icontains=query, available=True)
        
        if products.exists():
            response_text = f"Yes, {products.count()} product(s) found."
            product_list = [{
                'id': product.id,
                'slug': product.slug,  # Include slug in the response
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'image': product.image.url if product.image else None
            } for product in products]

            # Generate voice response
            audio_file_path = "static/audio/response.mp3"
            tts = gTTS(response_text)
            tts.save(audio_file_path)

            return JsonResponse({
                'message': response_text,
                'audio_url': '/' + audio_file_path,
                'products': product_list
            })
        else:
            response_text = "Sorry, no matching products found."
            audio_file_path = "static/audio/response.mp3"
            tts = gTTS(response_text)
            tts.save(audio_file_path)

            return JsonResponse({
                'message': response_text,
                'audio_url': '/' + audio_file_path,
                'products': []
            })

    return JsonResponse({'error': 'Invalid request'}, status=400)

def product_detail(request, slug):
    # Fetch the product by slug
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'assistant/product_detail.html', {'product': product})
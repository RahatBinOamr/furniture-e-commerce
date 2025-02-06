from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Contact
from shop.models import *
# Create your views here.
def homePage(request):
  products = Product.objects.all()[:3]
  context ={"products": products}
  return render(request, 'home.html',context)

def aboutPage(request):
  return render(request, 'about.html')

def servicePage(request):
  products = Product.objects.all()[:3]
  context ={"products": products}
  return render(request, 'services.html',context)

def contactPage(request):
    if request.method == 'POST':
        firstName = request.POST.get('f-name')
        lastName = request.POST.get('l-name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if firstName and lastName and email and message:  
            Contact.objects.create(
                first_name=firstName,
                last_name=lastName,
                email=email,
                message=message
            )
            messages.success(request, "Your contact information was sent successfully!")
            return redirect('contact')  # Prevent form resubmission on refresh
        else:
            messages.error(request, "All fields are required!")

    return render(request, 'contact.html')

def blogPage(request):
   return render(request, 'blog.html')
from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, Cart, CartItem
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm,CustomLoginForm




def home(request):
    products = Product.objects.all()
    return render(request,'ecomm/home.html',{'products': products})

def about(request):
    return render(request,'ecomm/about.html')

def contact(request):
    return render(request,'ecomm/contact.html')

def product_detail(request, product_id):
    # Retrieve the product by its ID or slug
    product = get_object_or_404(Product, pk=product_id)
    
    product_images = product.gallery.all()
    
    # Pass the product to the template
    return render(request, 'ecomm/product_detail.html', {'product': product,'product_images': product_images})

def product_list(request):
    products = Product.objects.all()
    price_filter = request.GET.get('price_filter')
    
    if price_filter == 'asc':
        products = products.order_by('price')  # Ascending price order
    elif price_filter == 'desc':
        products = products.order_by('-price')  # Descending price order


    # Paginate the products list (10 products per page)
    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')  # Get the page number from the URL query parameter
    page_obj = paginator.get_page(page_number)

    # Pass the paginated products to the template
    return render(request, 'ecomm/product_list.html', {'page_obj': page_obj})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product already exists in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        # If the product is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'{product.name} quantity increased in your cart.')
    else:
        messages.success(request, f'{product.name} has been added to your cart.')

    return redirect('product_detail', product_id=product.id)
    # View cart

def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = cart.items.all()
        total_price = sum(item.total_price for item in cart_items)
    else:
        cart_items = []
        total_price = 0
    return render(request, 'ecomm/cart.html', {'cart_items': cart_items, 'total_price': total_price})



# Remove an item from the cart

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'ecomm/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, f"Account created for success!")
            return redirect('home')  # Redirect to the homepage (or any other page you want)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'ecomm/register.html', {'form': form})



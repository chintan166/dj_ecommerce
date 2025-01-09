from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem, ContactUs, ShippingMethod, PaymentMethod, OrderItem
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm, ContactUsForm, CheckoutForm

# Home page displaying all products
def home(request):
    products = Product.objects.all()
    return render(request, 'ecomm/home.html', {'products': products})

# About page
def about(request):
    return render(request, 'ecomm/about.html')

# Product detail page
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_images = product.gallery.all()
    return render(request, 'ecomm/product_detail.html', {'product': product, 'product_images': product_images})

# List all products with price sorting and pagination
def product_list(request):
    products = Product.objects.all()
    price_filter = request.GET.get('price_filter')

    if price_filter == 'asc':
        products = products.order_by('price')
    elif price_filter == 'desc':
        products = products.order_by('-price')

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ecomm/product_list.html', {'page_obj': page_obj})

# Add product to cart (or increase quantity if already added)
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if item_created:
        messages.success(request, f'{product.name} has been added to your cart.')
    else:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Quantity of {product.name} increased by 1.')
        
    return redirect('product_detail', product_id=product.id)

# View the items in the cart
@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = cart.items.all()
        total_price = sum(item.total_price for item in cart_items)
    else:
        cart_items = []
        total_price = 0

    return render(request, 'ecomm/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Increment product quantity in the cart
@login_required
def increment_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f'Quantity of {cart_item.product.name} increased by 1.')
    return redirect('view_cart')

# Decrement product quantity in the cart (or remove item if quantity is 1)
@login_required
def decrement_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, f'Quantity of {cart_item.product.name} decreased by 1.')
    else:
        cart_item.delete()
        messages.warning(request, f'{cart_item.product.name} has been removed from your cart.')
    return redirect('view_cart')

# Checkout view to review cart and process the order
@login_required
def checkout_view(request):
    # Retrieve the user's cart
    cart = Cart.objects.filter(user=request.user).first()

    cart_items = []
    total_price = 0

    if cart:
        cart_items = cart.items.all()
        if cart_items:
            # Calculate the total price of all items in the cart
            total_price = sum(item.product.price * item.quantity for item in cart_items)
        else:
            messages.error(request, "Your cart is empty!")
            return redirect('view_cart')
    else:
        messages.error(request, "No cart found.")
        return redirect('home')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            shipping_method = form.cleaned_data['shipping_method']
            payment_method = form.cleaned_data['payment_method']

            try:
                # Create the order but don't save yet (commit=False)
                order = form.save(commit=False)
                order.user = request.user
                order.total_price = total_price + shipping_method.price  # Add shipping cost to total price
                order.save()  # Save the order to generate an ID

                # Now create the OrderItems for each CartItem
                for item in cart_items:
                    # Create an OrderItem for each item in the cart
                    OrderItem.objects.create(
                        order=order,  # Link to the Order
                        product=item.product,  # Link to the Product
                        quantity=item.quantity,  # Quantity from the cart
                        price=item.product.price  # Price of the product
                    )

                # Clear the cart after creating the order
                cart.items.all().delete()

                return redirect('order_success')  # Redirect to the order success page

            except Exception as e:
                print(f"Error during order creation: {e}")
                messages.error(request, f"There was an issue processing your order: {e}. Please try again.")
                return redirect('checkout')

        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, "There was an error with your checkout form. Please check and try again.")
    else:
        form = CheckoutForm()

    shipping_methods = ShippingMethod.objects.all()
    payment_methods = PaymentMethod.objects.all()

    return render(request, 'ecomm/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_methods': shipping_methods,
        'payment_methods': payment_methods
    })


# Success page after successful order
def order_success(request):
    return render(request, 'ecomm/order_success.html', {'message': 'Your order was successfully placed!'})

# Remove an item from the cart
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

# User login view
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

# User registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'ecomm/register.html', {'form': form})

# Contact form view
def contact_view(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contact_us = form.save(commit=False)
            contact_us.save()
            messages.success(request, 'Your message has been sent successfully!')

            return redirect('home')
    else:
        form = ContactUsForm()

    return render(request, 'ecomm/contact_form.html', {'form': form})

# Thank you page after contact submission
def contact_thanks(request):
    return render(request, 'ecomm/contact_thanks.html')
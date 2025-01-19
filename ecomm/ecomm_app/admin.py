from django.contrib import admin
from .models import Product,Color,Category,Cart,CartItem,ProductImage,CustomUser,ContactUs,ShippingMethod,PaymentMethod,Order

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    # Add quotes around 'id' to fix the syntax issue
    
    inlines = [ProductImageInline]
    
    list_display = ('name', 'description', 'price', 'image_tag', 'category','stock')  # Fixed issue with 'id' not being a string
    list_filter = ('price','category')

    def image_tag(self, obj):
        if obj.image:
            # Return the HTML <img> tag for rendering in the admin grid
            return f'<img src="{obj.image.url}" width="50" />'
        return 'No image'

    # Allow HTML rendering in the grid
    image_tag.allow_tags = True  # This is necessary for rendering HTML
    image_tag.short_description = 'Image'  # Custom column name for the image

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','total_price', 'ordered_at','billing_address','shipping_address','shipping_method','payment_method')
    search_fields = ('ordered_at',)
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','subject','message')
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username','email', 'first_name','last_name','address')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)
admin.site.register(Color)
admin.site.register(CartItem)
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(ContactUs,ContactUsAdmin)
admin.site.register(ShippingMethod)
admin.site.register(PaymentMethod)
admin.site.register(Order,OrderAdmin)
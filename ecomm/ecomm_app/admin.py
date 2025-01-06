from django.contrib import admin
from .models import Product,Category,Cart,CartItem,ProductImage,CustomUser,ContactUs

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    # Add quotes around 'id' to fix the syntax issue
    
    inlines = [ProductImageInline]
    
    list_display = ('name', 'description', 'price', 'image_tag', 'category')  # Fixed issue with 'id' not being a string
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
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','subject','message')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CustomUser)
admin.site.register(ContactUs,ContactUsAdmin)




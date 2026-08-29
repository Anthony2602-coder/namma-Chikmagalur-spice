from django.contrib import admin
from .models import (
    Category, Product, ProductImage, Address, Cart, Wishlist,
    Coupon, Order, OrderItem, Review, Banner, Newsletter,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "icon", "created_at"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "is_featured", "is_bestseller", "rating"]
    list_filter = ["category", "is_featured", "is_bestseller"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["full_name", "user", "city", "pincode", "is_default"]
    list_filter = ["state", "is_default"]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["code", "discount_percent", "min_order", "is_active", "valid_until"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product_name", "product_price", "quantity", "subtotal"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "user", "status", "total", "payment_method", "created_at"]
    list_filter = ["status", "payment_method", "payment_status"]
    search_fields = ["order_number", "user__username", "shipping_name"]
    inlines = [OrderItemInline]
    readonly_fields = ["order_number", "subtotal", "discount", "total", "created_at"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "rating", "title", "created_at"]
    list_filter = ["rating"]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "order"]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["email", "subscribed_at"]


admin.site.site_header = "Namma Chikmagaluru Admin"
admin.site.site_title = "NC Admin"
admin.site.index_title = "Store Management Dashboard"

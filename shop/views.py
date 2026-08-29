import uuid
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Avg, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    AddressForm, CheckoutForm, LoginForm, NewsletterForm,
    ReviewForm, SignUpForm,
)
from .models import (
    Address, Banner, Cart, Category, Coupon, Newsletter,
    Order, OrderItem, Product, Review, Wishlist,
)


def _ensure_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def _get_cart_queryset(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related("product")
    return Cart.objects.filter(session_key=_ensure_session(request)).select_related("product")


def _merge_session_cart(request):
    if not request.user.is_authenticated:
        return
    session_key = request.session.session_key
    if not session_key:
        return
    session_items = Cart.objects.filter(session_key=session_key)
    for item in session_items:
        existing, created = Cart.objects.get_or_create(
            user=request.user, product=item.product, defaults={"quantity": item.quantity}
        )
        if not created:
            existing.quantity += item.quantity
            existing.save()
        item.delete()


def home(request):
    banners = Banner.objects.filter(is_active=True)
    categories = Category.objects.all()
    featured = Product.objects.filter(is_featured=True)[:8]
    bestsellers = Product.objects.filter(is_bestseller=True)[:8]
    new_arrivals = Product.objects.all()[:8]
    newsletter_form = NewsletterForm()
    return render(request, "shop/home.html", {
        "banners": banners,
        "categories": categories,
        "featured": featured,
        "bestsellers": bestsellers,
        "new_arrivals": new_arrivals,
        "newsletter_form": newsletter_form,
    })


def product_list(request, category_slug=None):
    products = Product.objects.select_related("category").all()
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    q = request.GET.get("q", "").strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q) | Q(category__name__icontains=q)
        )

    sort = request.GET.get("sort", "")
    sort_map = {
        "price_low": "price",
        "price_high": "-price",
        "rating": "-rating",
        "newest": "-created_at",
    }
    products = products.order_by(sort_map.get(sort, "-is_featured"))

    categories = Category.objects.all()
    return render(request, "shop/product_list.html", {
        "products": products,
        "category": category,
        "categories": categories,
        "q": q,
        "sort": sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    reviews = product.reviews.select_related("user").all()
    related = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    review_form = ReviewForm() if request.user.is_authenticated else None
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user, product=product).first()
    return render(request, "shop/product_detail.html", {
        "product": product,
        "reviews": reviews,
        "related": related,
        "in_wishlist": in_wishlist,
        "review_form": review_form,
        "user_review": user_review,
    })


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity", 1))
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    else:
        session_key = _ensure_session(request)
        cart_item, created = Cart.objects.get_or_create(session_key=session_key, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    messages.success(request, f"{product.name} added to cart!")
    next_url = request.POST.get("next", "shop:cart")
    if next_url == "stay":
        return redirect("shop:product_detail", slug=product.slug)
    return redirect("shop:cart")


def cart_view(request):
    items = _get_cart_queryset(request)
    subtotal = sum(item.subtotal for item in items)
    shipping = Decimal("49.00") if subtotal < Decimal("499") and subtotal > 0 else Decimal("0")
    total = subtotal + shipping
    return render(request, "shop/cart.html", {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    })


@require_POST
def update_cart(request, item_id):
    item = get_object_or_404(Cart, pk=item_id)
    if request.user.is_authenticated and item.user != request.user:
        messages.error(request, "Unauthorized.")
        return redirect("shop:cart")
    if not request.user.is_authenticated and item.session_key != request.session.session_key:
        messages.error(request, "Unauthorized.")
        return redirect("shop:cart")
    action = request.POST.get("action")
    if action == "remove":
        item.delete()
        messages.info(request, "Item removed from cart.")
    elif action == "increase":
        item.quantity += 1
        item.save()
    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    return redirect("shop:cart")


@login_required
def checkout(request):
    items = _get_cart_queryset(request)
    if not items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("shop:product_list")

    subtotal = sum(item.subtotal for item in items)
    shipping = Decimal("49.00") if subtotal < Decimal("499") else Decimal("0")
    default_address = Address.objects.filter(user=request.user, is_default=True).first()

    initial = {}
    if default_address:
        initial = {
            "shipping_name": default_address.full_name,
            "shipping_phone": default_address.phone,
            "shipping_address": f"{default_address.address_line1}\n{default_address.address_line2}".strip(),
            "shipping_city": default_address.city,
            "shipping_state": default_address.state,
            "shipping_pincode": default_address.pincode,
        }

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            discount = Decimal("0")
            coupon = None
            coupon_code = form.cleaned_data.get("coupon_code", "").strip().upper()
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                    if subtotal >= coupon.min_order:
                        discount = (subtotal * Decimal(coupon.discount_percent)) / Decimal("100")
                    else:
                        messages.warning(request, f"Minimum order ₹{coupon.min_order} required for this coupon.")
                except Coupon.DoesNotExist:
                    messages.warning(request, "Invalid coupon code.")

            total = subtotal + shipping - discount
            order_number = f"NC{uuid.uuid4().hex[:8].upper()}"

            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    order_number=order_number,
                    shipping_name=form.cleaned_data["shipping_name"],
                    shipping_phone=form.cleaned_data["shipping_phone"],
                    shipping_address=form.cleaned_data["shipping_address"],
                    shipping_city=form.cleaned_data["shipping_city"],
                    shipping_state=form.cleaned_data["shipping_state"],
                    shipping_pincode=form.cleaned_data["shipping_pincode"],
                    payment_method=form.cleaned_data["payment_method"],
                    subtotal=subtotal,
                    discount=discount,
                    shipping_fee=shipping,
                    total=total,
                    coupon=coupon,
                    notes=form.cleaned_data.get("notes", ""),
                    status="confirmed",
                    payment_status="paid" if form.cleaned_data["payment_method"] != "cod" else "pending",
                )
                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        product_price=item.product.price,
                        quantity=item.quantity,
                        subtotal=item.subtotal,
                    )
                items.delete()

            messages.success(request, f"Order {order_number} placed successfully!")
            return redirect("shop:order_detail", order_number=order_number)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, "shop/checkout.html", {
        "form": form,
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": subtotal + shipping,
    })


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "shop/order_list.html", {"orders": orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "shop/order_detail.html", {"order": order})


@login_required
@require_POST
def cancel_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    if order.status in ("pending", "confirmed"):
        order.status = "cancelled"
        order.save()
        messages.info(request, "Order cancelled.")
    else:
        messages.error(request, "This order cannot be cancelled.")
    return redirect("shop:order_detail", order_number=order_number)


def signup_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("shop:profile")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            _merge_session_cart(request)
            messages.success(request, "Welcome to Namma Chikmagaluru!")
            return redirect("shop:home")
        messages.error(request, "Please fix the errors below to create your account.")
    else:
        form = SignUpForm()
    return render(request, "shop/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("shop:profile")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            _merge_session_cart(request)
            messages.success(request, "Logged in successfully!")
            next_url = request.POST.get("next") or request.GET.get("next") or "shop:home"
            if next_url.startswith("/"):
                return redirect(next_url)
            return redirect(next_url)
        messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "shop/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("shop:home")


@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)[:5]
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request, "shop/profile.html", {
        "addresses": addresses,
        "orders": orders,
        "wishlist_count": wishlist_count,
    })


@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if address.is_default:
                Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
            address.save()
            messages.success(request, "Address saved!")
            return redirect("shop:profile")
    else:
        form = AddressForm()
    return render(request, "shop/address_form.html", {"form": form, "title": "Add Address"})


@login_required
def edit_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            addr = form.save(commit=False)
            if addr.is_default:
                Address.objects.filter(user=request.user, is_default=True).exclude(pk=pk).update(is_default=False)
            addr.save()
            messages.success(request, "Address updated!")
            return redirect("shop:profile")
    else:
        form = AddressForm(instance=address)
    return render(request, "shop/address_form.html", {"form": form, "title": "Edit Address"})


@login_required
@require_POST
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.info(request, "Address deleted.")
    return redirect("shop:profile")


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "shop/wishlist.html", {"items": items})


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()
        messages.info(request, "Removed from wishlist.")
    else:
        messages.success(request, "Added to wishlist!")
    return redirect(request.POST.get("next", "shop:wishlist"))


@login_required
@require_POST
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if Review.objects.filter(user=request.user, product=product).exists():
        messages.warning(request, "You already reviewed this product.")
        return redirect("shop:product_detail", slug=slug)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
        avg = product.reviews.aggregate(avg=Avg("rating"))["avg"]
        product.rating = round(avg, 2)
        product.review_count = product.reviews.count()
        product.save()
        messages.success(request, "Thank you for your review!")
    return redirect("shop:product_detail", slug=slug)


@require_POST
def newsletter_subscribe(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Subscribed to newsletter!")
    else:
        messages.error(request, "Invalid or already subscribed email.")
    return redirect(request.POST.get("next", "shop:home"))


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    return render(request, "shop/contact.html")


def staff_check(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(staff_check)
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="pending").count()
    total_users = User.objects.count()
    recent_orders = Order.objects.select_related("user").all()[:10]
    low_stock = Product.objects.filter(stock__lte=10)
    return render(request, "shop/admin_dashboard.html", {
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_users": total_users,
        "recent_orders": recent_orders,
        "low_stock": low_stock,
    })


@login_required
@user_passes_test(staff_check)
def admin_product_edit(request, pk=None):
    from django import forms as django_forms

    class ProductForm(django_forms.ModelForm):
        class Meta:
            model = Product
            fields = [
                "category", "name", "description", "short_description", "price",
                "original_price", "stock", "weight", "image", "image_url",
                "is_featured", "is_bestseller", "origin",
            ]
            widgets = {
                "category": django_forms.Select(attrs={"class": "form-control"}),
                "name": django_forms.TextInput(attrs={"class": "form-control"}),
                "description": django_forms.Textarea(attrs={"class": "form-control", "rows": 4}),
                "short_description": django_forms.TextInput(attrs={"class": "form-control"}),
                "price": django_forms.NumberInput(attrs={"class": "form-control"}),
                "original_price": django_forms.NumberInput(attrs={"class": "form-control"}),
                "stock": django_forms.NumberInput(attrs={"class": "form-control"}),
                "weight": django_forms.TextInput(attrs={"class": "form-control"}),
                "image_url": django_forms.URLInput(attrs={"class": "form-control"}),
                "origin": django_forms.TextInput(attrs={"class": "form-control"}),
            }
    product = get_object_or_404(Product, pk=pk) if pk else None
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product saved!")
            return redirect("shop:admin_dashboard")
    else:
        form = ProductForm(instance=product)
    return render(request, "shop/admin_product_form.html", {
        "form": form,
        "product": product,
        "title": "Edit Product" if product else "Add Product",
    })


def install_app(request):
    return render(request, "shop/install.html")


def search_api(request):
    q = request.GET.get("q", "").strip()
    if len(q) < 2:
        return JsonResponse({"results": []})
    products = Product.objects.filter(name__icontains=q)[:8]
    results = [{"name": p.name, "slug": p.slug, "price": str(p.price), "image": p.display_image} for p in products]
    return JsonResponse({"results": results})

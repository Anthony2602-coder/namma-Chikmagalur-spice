import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Banner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("subtitle", models.CharField(blank=True, max_length=300)),
                ("image", models.ImageField(blank=True, null=True, upload_to="banners/")),
                ("image_url", models.URLField(blank=True)),
                ("link", models.CharField(blank=True, max_length=200)),
                ("is_active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("description", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="categories/")),
                ("icon", models.CharField(default="☕", max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"verbose_name_plural": "Categories", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=20, unique=True)),
                ("discount_percent", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ("min_order", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("is_active", models.BooleanField(default=True)),
                ("valid_until", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Newsletter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("subscribed_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("description", models.TextField()),
                ("short_description", models.CharField(blank=True, max_length=300)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ("original_price", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ("stock", models.PositiveIntegerField(default=100)),
                ("weight", models.CharField(blank=True, help_text="e.g. 250g, 500g, 1kg", max_length=50)),
                ("image", models.ImageField(blank=True, null=True, upload_to="products/")),
                ("image_url", models.URLField(blank=True, help_text="Fallback image URL if no upload")),
                ("is_featured", models.BooleanField(default=False)),
                ("is_bestseller", models.BooleanField(default=False)),
                ("rating", models.DecimalField(decimal_places=2, default=4.5, max_digits=3)),
                ("review_count", models.PositiveIntegerField(default=0)),
                ("origin", models.CharField(default="Chikmagaluru, Karnataka", max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="products", to="shop.category")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order_number", models.CharField(max_length=20, unique=True)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("processing", "Processing"), ("shipped", "Shipped"), ("delivered", "Delivered"), ("cancelled", "Cancelled")], default="pending", max_length=20)),
                ("payment_method", models.CharField(choices=[("cod", "Cash on Delivery"), ("upi", "UPI"), ("card", "Credit/Debit Card")], default="cod", max_length=20)),
                ("payment_status", models.CharField(default="pending", max_length=20)),
                ("shipping_name", models.CharField(max_length=100)),
                ("shipping_phone", models.CharField(max_length=15)),
                ("shipping_address", models.TextField()),
                ("shipping_city", models.CharField(max_length=100)),
                ("shipping_state", models.CharField(max_length=100)),
                ("shipping_pincode", models.CharField(max_length=10)),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=10)),
                ("discount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("shipping_fee", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("total", models.DecimalField(decimal_places=2, max_digits=10)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("coupon", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="shop.coupon")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="orders", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=15)),
                ("address_line1", models.CharField(max_length=255)),
                ("address_line2", models.CharField(blank=True, max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("pincode", models.CharField(max_length=10)),
                ("is_default", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="addresses", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name_plural": "Addresses", "ordering": ["-is_default", "-created_at"]},
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(blank=True, max_length=40)),
                ("quantity", models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ("added_at", models.DateTimeField(auto_now_add=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="shop.product")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="cart_items", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_name", models.CharField(max_length=200)),
                ("product_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantity", models.PositiveIntegerField()),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=10)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="shop.order")),
                ("product", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="shop.product")),
            ],
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="products/extra/")),
                ("alt_text", models.CharField(blank=True, max_length=200)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="extra_images", to="shop.product")),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("title", models.CharField(max_length=200)),
                ("comment", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="shop.product")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Wishlist",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("added_at", models.DateTimeField(auto_now_add=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="shop.product")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="wishlist_items", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="wishlist",
            unique_together={("user", "product")},
        ),
        migrations.AlterUniqueTogether(
            name="review",
            unique_together={("product", "user")},
        ),
        migrations.AlterUniqueTogether(
            name="cart",
            unique_together={("user", "product"), ("session_key", "product")},
        ),
    ]

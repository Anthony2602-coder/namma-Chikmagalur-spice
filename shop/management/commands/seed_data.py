from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product, Coupon, Banner


PRODUCTS = {
    "Coffee": [
        ("Arabica Estate Coffee - 250g", "Premium single-origin Arabica from Chikmagaluru hills. Medium roast with notes of chocolate and caramel.", 349, 449, "250g"),
        ("Robusta Bold Coffee - 500g", "Strong and rich Robusta blend perfect for filter coffee lovers.", 499, 599, "500g"),
        ("Monsoon Malabar Coffee - 1kg", "Traditional monsoon-processed coffee with earthy, mellow flavour.", 899, 1099, "1kg"),
        ("Filter Coffee Powder - 200g", "Classic South Indian filter coffee decoction mix.", 199, 249, "200g"),
        ("Organic Green Coffee Beans - 500g", "Unroasted green beans for health-conscious brewers.", 449, None, "500g"),
        ("Dark Roast Espresso Blend - 250g", "Intense dark roast ideal for espresso machines.", 399, 479, "250g"),
    ],
    "Black Pepper": [
        ("Malabar Black Pepper - 100g", "World-famous Malabar peppercorns with bold, pungent aroma from Chikmagaluru.", 149, 199, "100g"),
        ("Tellicherry Pepper - 250g", "Extra-large premium Tellicherry peppercorns, hand-picked.", 349, 429, "250g"),
        ("Organic Whole Pepper - 500g", "Certified organic whole black pepper, sun-dried.", 599, 699, "500g"),
        ("Pepper Powder - 100g", "Freshly ground pepper powder for everyday cooking.", 129, 159, "100g"),
        ("Pepper & Coffee Gift Box", "Curated gift set with premium coffee and Malabar pepper.", 799, 999, "Combo"),
        ("Smoked Black Pepper - 200g", "Unique smoked pepper with deep woody notes.", 279, 349, "200g"),
    ],
}

IMAGE_URLS = {
    "Coffee": [
        "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=600",
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600",
        "https://images.unsplash.com/photo-1514434755168-3e3e4e4b4b4b?w=600",
        "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600",
        "https://images.unsplash.com/photo-1559056199-641a0ac8b55c?w=600",
        "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=600",
    ],
    "Black Pepper": [
        "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=600",
        "https://images.unsplash.com/photo-1615485290382-44100d3a38fd?w=600",
        "https://images.unsplash.com/photo-1599909538395-2d5170d2b712?w=600",
        "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=600",
        "https://images.unsplash.com/photo-1559056199-641a0ac8b55c?w=600",
        "https://images.unsplash.com/photo-1615485290382-44100d3a38fd?w=600",
    ],
}


class Command(BaseCommand):
    help = "Seed sample data for Namma Chikmagaluru"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@nammachikmagaluru.in", "admin123")
            self.stdout.write(self.style.SUCCESS("Created superuser: admin / admin123"))

        coffee, _ = Category.objects.get_or_create(
            name="Coffee", defaults={"description": "Premium Chikmagaluru coffee", "icon": "☕"}
        )
        pepper, _ = Category.objects.get_or_create(
            name="Black Pepper", defaults={"description": "Authentic Malabar black pepper", "icon": "🌶️"}
        )

        cats = {"Coffee": coffee, "Black Pepper": pepper}
        for cat_name, products in PRODUCTS.items():
            cat = cats[cat_name]
            urls = IMAGE_URLS[cat_name]
            for i, (name, desc, price, orig, weight) in enumerate(products):
                Product.objects.update_or_create(
                    name=name,
                    defaults={
                        "category": cat,
                        "description": desc,
                        "short_description": desc[:120],
                        "price": price,
                        "original_price": orig,
                        "weight": weight,
                        "image_url": urls[i % len(urls)],
                        "is_featured": i < 3,
                        "is_bestseller": i % 2 == 0,
                        "stock": 100,
                        "rating": 4.2 + (i % 8) * 0.1,
                        "review_count": 10 + i * 5,
                    },
                )

        Coupon.objects.get_or_create(
            code="CHIKMAGALURU10",
            defaults={"discount_percent": 10, "min_order": 299, "is_active": True},
        )
        Coupon.objects.get_or_create(
            code="FIRST50",
            defaults={"discount_percent": 50, "min_order": 999, "is_active": True},
        )

        if not Banner.objects.exists():
            Banner.objects.create(
                title="Fresh from Chikmagaluru Hills",
                subtitle="Premium Coffee & Malabar Black Pepper delivered to your doorstep",
                image_url="https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=1200",
                link="/products/",
                order=1,
            )
            Banner.objects.create(
                title="Monsoon Malabar Special",
                subtitle="Up to 30% off on select coffee blends",
                image_url="https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=1200",
                link="/products/category/coffee/",
                order=2,
            )
            Banner.objects.create(
                title="Authentic Malabar Pepper",
                subtitle="Hand-picked, sun-dried, straight from Karnataka",
                image_url="https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=1200",
                link="/products/category/black-pepper/",
                order=3,
            )

        self.stdout.write(self.style.SUCCESS("Seed data loaded successfully!"))

from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Category, Product
from datetime import date


class Command(BaseCommand):
    help = "Add test products to the database"

    def handle(self, *args, **kwargs):
        with transaction.atomic():

            self.stdout.write(self.style.NOTICE("Deleting existing data..."))
            Product.objects.all().delete()
            Category.objects.all().delete()

            categories = [
                {
                    "name": "Guitars",
                    "description": "Stringed musical instruments with a fretted neck.",
                },
                {
                    "name": "Drums",
                    "description": "Percussion instruments used in various music genres.",
                },
                {
                    "name": "Pianos",
                    "description": "Keyboard instruments with hammers and strings.",
                },
                {
                    "name": "Violins",
                    "description": "String instruments played with a bow.",
                },
                {
                    "name": "Saxophones",
                    "description": "Brass instruments with a single-reed mouthpiece.",
                },
            ]

            for cat_data in categories:
                category, created = Category.objects.get_or_create(**cat_data)
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully added category: {category.name}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Category already exists: {category.name}")
                    )

            products = [
                {
                    "name": "Fender Stratocaster",
                    "description": "Electric guitar with three single-coil pickups.",
                    "image": "fender_stratocaster.jpg",
                    "category": Category.objects.get(name="Guitars"),
                    "price": 1200.00,
                    "created_at": date(2024, 9, 10),
                    "updated_at": date(2024, 9, 12),
                },
                {
                    "name": "Gibson Les Paul",
                    "description": "Electric guitar known for its thick, creamy sound.",
                    "image": "gibson_les_paul.jpg",
                    "category": Category.objects.get(name="Guitars"),
                    "price": 1500.00,
                    "created_at": date(2024, 9, 11),
                    "updated_at": date(2024, 9, 13),
                },
                {
                    "name": "Roland TD-17",
                    "description": "Electronic drum kit with advanced features.",
                    "image": "roland_td17.jpg",
                    "category": Category.objects.get(name="Drums"),
                    "price": 800.00,
                    "created_at": date(2024, 9, 12),
                    "updated_at": date(2024, 9, 14),
                },
                {
                    "name": "Yamaha P-125",
                    "description": "Digital piano with weighted keys and built-in speakers.",
                    "image": "yamaha_p125.jpg",
                    "category": Category.objects.get(name="Pianos"),
                    "price": 700.00,
                    "created_at": date(2024, 9, 13),
                    "updated_at": date(2024, 9, 15),
                },
                {
                    "name": "Stradivarius Violin",
                    "description": "High-quality violin crafted by Antonio Stradivari.",
                    "image": "stradivarius_violin.jpg",
                    "category": Category.objects.get(name="Violins"),
                    "price": 5000.00,
                    "created_at": date(2024, 9, 14),
                    "updated_at": date(2024, 9, 16),
                },
            ]

            for prod_data in products:
                category, _ = Category.objects.get_or_create(
                    name=prod_data["category_name"]
                )
                product, created = Product.objects.get_or_create(
                    name=prod_data["name"],
                    description=prod_data["description"],
                    image=prod_data["image"],
                    category=category,
                    price=prod_data["price"],
                    created_at=prod_data["created_at"],
                    updated_at=prod_data["updated_at"],
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully added product: {product.name}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Product already exists: {product.name}")
                    )

"""
Management command to seed the database with sample data for Nepal Mart.
Usage: python3 manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Seed the database with sample categories and products for Nepal Mart'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create categories
        categories_data = [
            {'name': 'Groceries', 'description': 'Daily grocery items including rice, dal, spices, and more'},
            {'name': 'Beverages', 'description': 'Soft drinks, juices, tea, coffee, and water'},
            {'name': 'Snacks', 'description': 'Chips, biscuits, namkeen, and quick bites'},
            {'name': 'Dairy Products', 'description': 'Milk, curd, paneer, cheese, and butter'},
            {'name': 'Personal Care', 'description': 'Soaps, shampoo, toothpaste, and skincare'},
            {'name': 'Household', 'description': 'Cleaning supplies, detergents, and home essentials'},
            {'name': 'Fruits & Vegetables', 'description': 'Fresh fruits and vegetables'},
            {'name': 'Frozen Foods', 'description': 'Frozen momos, ice cream, and ready-to-cook items'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'is_active': True,
                }
            )
            categories[cat_data['name']] = cat
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f"  Category: {cat.name} - {status}")

        # Create products
        products_data = [
            # Groceries
            {'name': 'Basmati Rice (5kg)', 'category': 'Groceries', 'price': 850, 'sku': 'GR-001', 'stock': 50, 'unit': 'packet'},
            {'name': 'Toor Dal (1kg)', 'category': 'Groceries', 'price': 220, 'sku': 'GR-002', 'stock': 80, 'unit': 'packet'},
            {'name': 'Mustard Oil (1L)', 'category': 'Groceries', 'price': 340, 'sku': 'GR-003', 'stock': 60, 'unit': 'piece'},
            {'name': 'Turmeric Powder (200g)', 'category': 'Groceries', 'price': 85, 'sku': 'GR-004', 'stock': 100, 'unit': 'packet'},
            {'name': 'Salt (1kg)', 'category': 'Groceries', 'price': 30, 'sku': 'GR-005', 'stock': 150, 'unit': 'packet'},
            {'name': 'Sugar (1kg)', 'category': 'Groceries', 'price': 120, 'sku': 'GR-006', 'stock': 90, 'unit': 'packet'},
            {'name': 'Atta Flour (5kg)', 'category': 'Groceries', 'price': 450, 'sku': 'GR-007', 'stock': 40, 'unit': 'packet'},
            {'name': 'Chilli Powder (200g)', 'category': 'Groceries', 'price': 95, 'sku': 'GR-008', 'stock': 70, 'unit': 'packet'},

            # Beverages
            {'name': 'Coca-Cola (500ml)', 'category': 'Beverages', 'price': 60, 'sku': 'BV-001', 'stock': 200, 'unit': 'piece'},
            {'name': 'Real Juice Mango (1L)', 'category': 'Beverages', 'price': 160, 'sku': 'BV-002', 'stock': 80, 'unit': 'piece'},
            {'name': 'Tokla Green Tea (25 bags)', 'category': 'Beverages', 'price': 180, 'sku': 'BV-003', 'stock': 60, 'unit': 'box'},
            {'name': 'Nescafe Classic (100g)', 'category': 'Beverages', 'price': 350, 'sku': 'BV-004', 'stock': 45, 'unit': 'piece'},
            {'name': 'Mineral Water (1L)', 'category': 'Beverages', 'price': 25, 'sku': 'BV-005', 'stock': 300, 'unit': 'piece'},

            # Snacks
            {'name': 'Wai Wai Noodles', 'category': 'Snacks', 'price': 25, 'sku': 'SN-001', 'stock': 500, 'unit': 'piece', 'featured': True},
            {'name': 'Lays Classic Chips', 'category': 'Snacks', 'price': 50, 'sku': 'SN-002', 'stock': 120, 'unit': 'packet'},
            {'name': 'Bourbon Biscuit', 'category': 'Snacks', 'price': 40, 'sku': 'SN-003', 'stock': 100, 'unit': 'packet'},
            {'name': 'Bhujia Namkeen (200g)', 'category': 'Snacks', 'price': 75, 'sku': 'SN-004', 'stock': 80, 'unit': 'packet'},
            {'name': 'Current Noodles', 'category': 'Snacks', 'price': 15, 'sku': 'SN-005', 'stock': 400, 'unit': 'piece'},

            # Dairy
            {'name': 'DDC Milk (500ml)', 'category': 'Dairy Products', 'price': 50, 'sku': 'DR-001', 'stock': 100, 'unit': 'piece', 'featured': True},
            {'name': 'DDC Curd (500g)', 'category': 'Dairy Products', 'price': 65, 'sku': 'DR-002', 'stock': 50, 'unit': 'piece'},
            {'name': 'Amul Butter (100g)', 'category': 'Dairy Products', 'price': 85, 'sku': 'DR-003', 'stock': 40, 'unit': 'piece'},
            {'name': 'Paneer (200g)', 'category': 'Dairy Products', 'price': 120, 'sku': 'DR-004', 'stock': 30, 'unit': 'piece'},
            {'name': 'Cheese Slice (10 pcs)', 'category': 'Dairy Products', 'price': 200, 'sku': 'DR-005', 'stock': 25, 'unit': 'packet'},

            # Personal Care
            {'name': 'Lifebuoy Soap (100g)', 'category': 'Personal Care', 'price': 45, 'sku': 'PC-001', 'stock': 150, 'unit': 'piece'},
            {'name': 'Dove Shampoo (200ml)', 'category': 'Personal Care', 'price': 280, 'sku': 'PC-002', 'stock': 60, 'unit': 'piece'},
            {'name': 'Colgate Toothpaste (150g)', 'category': 'Personal Care', 'price': 120, 'sku': 'PC-003', 'stock': 90, 'unit': 'piece'},
            {'name': 'Dettol Handwash (250ml)', 'category': 'Personal Care', 'price': 160, 'sku': 'PC-004', 'stock': 70, 'unit': 'piece'},

            # Household
            {'name': 'Surf Excel (1kg)', 'category': 'Household', 'price': 220, 'sku': 'HH-001', 'stock': 80, 'unit': 'packet'},
            {'name': 'Vim Dishwash (500ml)', 'category': 'Household', 'price': 130, 'sku': 'HH-002', 'stock': 60, 'unit': 'piece'},
            {'name': 'Harpic (500ml)', 'category': 'Household', 'price': 180, 'sku': 'HH-003', 'stock': 50, 'unit': 'piece'},
            {'name': 'Room Freshener', 'category': 'Household', 'price': 250, 'sku': 'HH-004', 'stock': 35, 'unit': 'piece'},

            # Fruits & Vegetables
            {'name': 'Banana (1 dozen)', 'category': 'Fruits & Vegetables', 'price': 120, 'sku': 'FV-001', 'stock': 40, 'unit': 'dozen', 'featured': True},
            {'name': 'Apple (1kg)', 'category': 'Fruits & Vegetables', 'price': 350, 'sku': 'FV-002', 'stock': 30, 'unit': 'kg'},
            {'name': 'Tomato (1kg)', 'category': 'Fruits & Vegetables', 'price': 80, 'sku': 'FV-003', 'stock': 50, 'unit': 'kg'},
            {'name': 'Onion (1kg)', 'category': 'Fruits & Vegetables', 'price': 60, 'sku': 'FV-004', 'stock': 70, 'unit': 'kg'},
            {'name': 'Potato (1kg)', 'category': 'Fruits & Vegetables', 'price': 45, 'sku': 'FV-005', 'stock': 100, 'unit': 'kg'},

            # Frozen Foods
            {'name': 'Frozen Momos (10 pcs)', 'category': 'Frozen Foods', 'price': 250, 'sku': 'FF-001', 'stock': 30, 'unit': 'packet', 'featured': True},
            {'name': 'Ice Cream Vanilla (1L)', 'category': 'Frozen Foods', 'price': 320, 'sku': 'FF-002', 'stock': 20, 'unit': 'piece'},
            {'name': 'Frozen French Fries (500g)', 'category': 'Frozen Foods', 'price': 180, 'sku': 'FF-003', 'stock': 25, 'unit': 'packet'},
        ]

        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                sku=prod_data['sku'],
                defaults={
                    'name': prod_data['name'],
                    'slug': slugify(prod_data['name']),
                    'category': categories[prod_data['category']],
                    'price': prod_data['price'],
                    'stock_quantity': prod_data['stock'],
                    'unit': prod_data.get('unit', 'piece'),
                    'is_active': True,
                    'is_featured': prod_data.get('featured', False),
                    'minimum_stock': 5,
                }
            )
            if created:
                self.stdout.write(f"  Product: {product.name} - Rs.{product.price}")

        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@nepalmart.com',
                password='admin123',
                first_name='Admin',
                last_name='Nepal Mart'
            )
            self.stdout.write(self.style.SUCCESS('  Superuser created: admin / admin123'))

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'  Categories: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  Products: {Product.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'\n  Admin Login: username=admin, password=admin123'))

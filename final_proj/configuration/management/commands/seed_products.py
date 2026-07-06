from decimal import Decimal

from django.core.management.base import BaseCommand

from configuration.models import Category, Item


PRODUCTS = {
    'electronics': {
        'name': 'Electronics',
        'items': [
            {
                'name': 'iPhone 15',
                'description': 'Apple smartphone with a bright display and fast camera.',
                'price': Decimal('39999.00'),
                'quantity': 8,
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Android smartphone with AMOLED display and powerful processor.',
                'price': Decimal('36999.00'),
                'quantity': 10,
            },
            {
                'name': 'MacBook Air M2',
                'description': 'Lightweight laptop for study, work, and everyday tasks.',
                'price': Decimal('52999.00'),
                'quantity': 5,
            },
            {
                'name': 'Sony WH-1000XM5',
                'description': 'Wireless headphones with active noise cancellation.',
                'price': Decimal('12999.00'),
                'quantity': 12,
            },
        ],
    },
    'clothing': {
        'name': 'Clothing',
        'items': [
            {
                'name': 'Basic Cotton T-Shirt',
                'description': 'Comfortable everyday T-shirt made from soft cotton.',
                'price': Decimal('699.00'),
                'quantity': 30,
            },
            {
                'name': 'Black Hoodie',
                'description': 'Warm hoodie with a minimal design and front pocket.',
                'price': Decimal('1899.00'),
                'quantity': 18,
            },
            {
                'name': 'Slim Fit Jeans',
                'description': 'Classic blue jeans for casual outfits.',
                'price': Decimal('2199.00'),
                'quantity': 16,
            },
            {
                'name': 'Running Sneakers',
                'description': 'Light sneakers for walking, sport, and daily use.',
                'price': Decimal('3299.00'),
                'quantity': 14,
            },
        ],
    },
    'home-appliances': {
        'name': 'Home Appliances',
        'items': [
            {
                'name': 'Electric Kettle',
                'description': 'Fast-boiling kettle with automatic shutoff.',
                'price': Decimal('1199.00'),
                'quantity': 20,
            },
            {
                'name': 'Robot Vacuum Cleaner',
                'description': 'Smart vacuum cleaner for automatic home cleaning.',
                'price': Decimal('8999.00'),
                'quantity': 7,
            },
            {
                'name': 'Microwave Oven',
                'description': 'Compact microwave oven for quick heating and cooking.',
                'price': Decimal('4499.00'),
                'quantity': 9,
            },
        ],
    },
}


class Command(BaseCommand):
    help = 'Seed the database with sample categories and products.'

    def handle(self, *args, **options):
        created_categories = 0
        created_items = 0
        updated_items = 0

        for slug, category_data in PRODUCTS.items():
            category, category_created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': category_data['name']},
            )
            if category_created:
                created_categories += 1

            for item_data in category_data['items']:
                item, item_created = Item.objects.update_or_create(
                    name=item_data['name'],
                    defaults={
                        'description': item_data['description'],
                        'category': category,
                        'price': item_data['price'],
                        'quantity': item_data['quantity'],
                    },
                )

                if item_created:
                    created_items += 1
                else:
                    updated_items += 1

        self.stdout.write(
            self.style.SUCCESS(
                'Seed completed: '
                f'{created_categories} categories created, '
                f'{created_items} products created, '
                f'{updated_items} products updated.'
            )
        )

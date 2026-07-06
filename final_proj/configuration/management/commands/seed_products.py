from io import BytesIO
from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image, ImageDraw, ImageFont

from configuration.models import Category, Item


CATEGORY_STYLES = {
    'electronics': {
        'background': '#0f172a',
        'accent': '#38bdf8',
    },
    'clothing': {
        'background': '#2d1b4e',
        'accent': '#f472b6',
    },
    'home-appliances': {
        'background': '#14532d',
        'accent': '#86efac',
    },
}


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


def create_product_image(product_name, category_name, background, accent):
    image = Image.new('RGB', (640, 420), background)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    draw.rounded_rectangle((32, 32, 608, 388), radius=28, outline=accent, width=6)
    draw.rectangle((32, 290, 608, 388), fill=accent)

    title = product_name[:32]
    category = category_name.upper()

    title_box = draw.textbbox((0, 0), title, font=font)
    title_width = title_box[2] - title_box[0]
    draw.text(((640 - title_width) / 2, 170), title, fill='white', font=font)

    category_box = draw.textbbox((0, 0), category, font=font)
    category_width = category_box[2] - category_box[0]
    draw.text(((640 - category_width) / 2, 330), category, fill='black', font=font)

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = 'Seed the database with sample categories and products.'

    def handle(self, *args, **options):
        created_categories = 0
        created_items = 0
        updated_items = 0
        created_images = 0

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

                if not item.image:
                    style = CATEGORY_STYLES[slug]
                    image_file = create_product_image(
                        item.name,
                        category.name,
                        style['background'],
                        style['accent'],
                    )
                    image_name = f'seed/{slugify(item.name)}.png'
                    item.image.save(image_name, image_file, save=True)
                    created_images += 1

        self.stdout.write(
            self.style.SUCCESS(
                'Seed completed: '
                f'{created_categories} categories created, '
                f'{created_items} products created, '
                f'{updated_items} products updated, '
                f'{created_images} product images created.'
            )
        )

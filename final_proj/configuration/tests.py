from django.test import TestCase
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Item, Order, OrderItem
from .forms import LoginForm


User = get_user_model()


class ModelTests(TestCase):
    def test_cathegory_model(self):
        category = Category.objects.create(name='Smartphones', slug='smartphones')
        self.assertEqual(str(category), 'Smartphones')

    def test_item_str_returns_name(self):
        category = Category.objects.create(name='Smartphones', slug='smartphones')
        item = Item.objects.create(
            name='Iphone 15',
            description='Best value for money',
            category=category,
            price=Decimal('1000.00'),
            image='items/iphone15.jpg',
            quantity=10,
        )
        self.assertEqual(str(item), 'Iphone 15')


class LoginFormTests(TestCase):
    def test_login_form_valid(self):
        form = LoginForm(data={'email': 'test@example.com', 'password': '1234567890'})
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_email(self):
        form = LoginForm(data={'email': 'invalid_email', 'password': '1234567890'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class ViewTests(TestCase):

    def test_main_page_redirects_anonymous_user_to_login(self):
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
        
    def test_main_page_available_for_logged_in_user(self):
        user = User.objects.create_user(
            email='user@example.com',
            username='user',
            password='strong-password',
        )
        
        self.client.login(email='user@example.com', password='strong-password')
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)

    def test_buy_item_creates_order_for_logged_in_user(self):
        user = User.objects.create_user(
            email='buyer@example.com',
            username='buyer',
            password='strong-password',
        )
        category = Category.objects.create(name='Smartphones', slug='phones')
        item = Item.objects.create(
            name='Iphone 15',
            description='Best value for money',
            category=category,
            price=Decimal('1000.00'),
            image='items/iphone15.jpg',
            quantity=10,
        )

        self.client.login(email='buyer@example.com', password='strong-password')
        response = self.client.post(reverse('buy_item', args=[item.id]))

        self.assertRedirects(response, reverse('my_orders'))
        order = Order.objects.get(user=user)
        order_item = OrderItem.objects.get(order=order)
        self.assertEqual(order.total_price, item.price)
        self.assertEqual(order_item.item, item)
        self.assertEqual(order_item.quantity, 1)
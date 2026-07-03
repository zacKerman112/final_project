from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page_view, name='main_page'),
    path('buy/<int:item_id>/', views.buy_item_view, name='buy_item'),
    path('profile/', views.profile_view, name='profile'),
    path('my_orders/', views.my_orders_view, name='my_orders'),
    path('cart/', views.cart_view, name='cart'),
    path('settings/', views.settings_view, name='settings'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
]
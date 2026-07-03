from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'telegram_id', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom fields', {'fields': ('telegram_id', 'avatar')}),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
    

admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
from django.contrib import admin

from .models import Customer, Order, OrderItem, Product, Shipping
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    pass  # Để sử dụng cài đặt mặc định của UserAdmin

# Đăng ký model người dùng tùy chỉnh với trang quản trị
admin.site.register(Customer, CustomUserAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Shipping)
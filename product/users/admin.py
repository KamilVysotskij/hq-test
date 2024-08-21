from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, Balance, Subscription, StudentInGroup


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
    )


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')
    list_filter = ('user',)
    search_fields = ('user__email',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    list_filter = ('user', 'course')
    search_fields = ('user__email', 'course__title')


@admin.register(StudentInGroup)
class StudentInGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')
    list_filter = ('user', 'group')
    search_fields = ('user__email', 'group__title')
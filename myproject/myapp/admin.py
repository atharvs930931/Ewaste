from django.contrib import admin
from .models import UserProfile, EWaste


# =========================
# UserProfile Admin
# =========================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)


# =========================
# EWaste Admin
# =========================
@admin.register(EWaste)
class EWasteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recycler',
        'category',
        'condition',
        'weight',
        'status',
        'created_at'
    )

    list_filter = ('status', 'category', 'condition')
    search_fields = ('user__username', 'location')
    readonly_fields = ('created_at',)

    ordering = ('-created_at',)

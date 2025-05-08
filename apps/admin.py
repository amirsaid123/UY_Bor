from django.contrib import admin

from apps.models import Category, Transaction


class AdminCategoty(admin.ModelAdmin):
    pass

admin.site.register(Transaction)

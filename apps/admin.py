from django.contrib import admin

from apps.models import Category


class AdminCategoty(admin.ModelAdmin):
    pass

admin.site.register(Category)

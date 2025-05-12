from django.contrib import admin
from .models import (
    User, Property, Blog,
    Video, ResidentialComplex, Amenity, Category, Image, Tariff,
    StaticPage, Metro, Country, Region, City, District
)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'first_name', 'last_name', 'role', 'balance',
                    'organization', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('phone_number', 'first_name', 'last_name')


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'price', 'status', 'user')
    list_filter = ('type', 'status', 'residential_complex', 'label', 'city', 'region', 'metro', 'district',
                   'created_at')
    search_fields = ('name', 'address', 'description')


class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title', 'description')
    exclude = ('slug',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    search_fields = ('name',)
    exclude = ('slug',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    search_fields = ('name',)
    exclude = ('slug',)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    exclude = ('slug',)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    search_fields = ('name',)
    exclude = ('slug',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'property')


class MetroAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    exclude = ('slug',)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name',)
    exclude = ('slug',)


class ResidentialComplexAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    exclude = ('slug',)


class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title', 'content')
    exclude = ('slug',)


class TariffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration_days', 'status', 'label', 'user')
    list_filter = ('status', 'label',)
    search_fields = ('name',)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'property')


admin.site.register(User, UserAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(ResidentialComplex, ResidentialComplexAdmin)
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(StaticPage, StaticPageAdmin)
admin.site.register(Metro, MetroAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)

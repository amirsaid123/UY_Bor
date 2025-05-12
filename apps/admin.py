from django.contrib import admin

from .models import (
    User, Property, Wishlist, Message, PhoneVerification, Transaction, Blog,
    Video, ResidentialComplex, Amenity, Category, Image, Tariff,
    StaticPage, Metro, Country, Region, City, District
)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'first_name', 'last_name', 'role',  'is_active', 'is_staff')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name')


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'price', 'status', 'user')
    list_filter = ('type', 'status', 'city')
    search_fields = ('name', 'address', 'description')


admin.site.register(User, UserAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Wishlist)
admin.site.register(Message)
admin.site.register(PhoneVerification)
admin.site.register(Transaction)
admin.site.register(Blog)
admin.site.register(Video)
admin.site.register(ResidentialComplex)
admin.site.register(Amenity)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Tariff)
admin.site.register(StaticPage)
admin.site.register(Metro)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(District)

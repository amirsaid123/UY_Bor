from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import CASCADE
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    organization = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    role = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    card_number = models.CharField(max_length=16, unique=True, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number


class Property(models.Model):
    class Material(models.TextChoices):
        BRICK = 'brick', 'Brick'
        MONOLITHIC = 'monolithic', 'Monolithic'
        CONCRETE_BLOCKS = 'concrete_blocks', 'Concrete Blocks'
        CONCRETE = 'concrete', 'Concrete'
        ANOTHER = 'another', 'Another'

    class Renovation(models.TextChoices):
        AUTHOR = 'author', 'Author design'
        EURO = 'euro', 'Euro renovation'
        MID = 'mid', 'Medium renovation'
        REQUIRED = 'required', 'Needs renovation'
        BLACK_PLASTER = 'black_plaster', 'Bare walls (Black plaster)'

    class Repair(models.TextChoices):
        AUTHOR = 'author', 'Author design'
        DECORATED = 'decorated', 'Decorated'
        REQUIRES_DECORATION = 'requires_decoration', 'Requires decoration'
        WITHOUT_DECORATION = 'without_decoration', 'Without decoration'

    class Type(models.TextChoices):
        SALE = 'sale', 'Sale'
        RENT = 'rent', 'Rent'

    class Label(models.TextChoices):
        VIP = 'vip', 'VIP'
        PREMIUM = 'premium', 'Premium'
        URGENT = 'urgent', 'Urgent'

    class ResidentialType(models.TextChoices):
        FREE_LAYOUT = 'free_layout', 'Free layout'
        ON_TIME = 'on_time', 'On time'
        FINISHED = 'finished', 'Finished'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        MODERATION = 'moderation', 'Moderation'
        CANCELED = 'canceled', 'Canceled'

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    building_material = models.CharField(max_length=100, choices=Material.choices)
    renovation_needed = models.CharField(max_length=100, choices=Renovation.choices)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    room = models.PositiveIntegerField()
    floor = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField(null=True, blank=True)
    amenities = models.ManyToManyField('apps.Amenity', related_name='properties', blank=True)
    type = models.CharField(max_length=10, choices=Type.choices)
    category = models.ForeignKey('apps.Category', on_delete=models.CASCADE, related_name='properties')
    label = models.CharField(max_length=10, choices=Label.choices, null=True, blank=True)
    repair = models.CharField(max_length=100, choices=Repair.choices, null=True, blank=True)

    residential_complex = models.ForeignKey('apps.ResidentialComplex', on_delete=CASCADE, null=True, blank=True)
    residential_type = models.CharField(max_length=100, choices=ResidentialType.choices, null=True, blank=True)
    commissioning_date = models.DateField(null=True, blank=True)

    views = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)

    city = models.ForeignKey('apps.City', on_delete=models.CASCADE, related_name='properties')
    region = models.ForeignKey('apps.Region', on_delete=models.CASCADE, related_name='properties')
    metro = models.ForeignKey('apps.Metro', on_delete=models.CASCADE, related_name='properties', null=True, blank=True)
    district = models.ForeignKey('apps.District', on_delete=models.CASCADE, related_name='properties', null=True,
                                 blank=True)
    country = models.ForeignKey('apps.Country', on_delete=models.CASCADE, related_name='properties', null=True,
                                blank=True)

    user = models.ForeignKey('apps.User', on_delete=models.CASCADE, related_name='properties')

    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    property = models.ForeignKey('apps.Property', on_delete=models.CASCADE, related_name='wishlist')
    user = models.ForeignKey('apps.User', on_delete=models.CASCADE, related_name='wishlist')


class Message(models.Model):
    receiver = models.ForeignKey('apps.User', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('apps.User', on_delete=models.CASCADE, related_name='sent_messages', null=True,
                               blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class PhoneVerification(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.code}"


class Transaction(models.Model):
    user = models.ForeignKey('apps.User', on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='blogs', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Video(models.Model):
    video = models.URLField()
    property = models.ForeignKey('apps.Property', on_delete=models.CASCADE, related_name='videos')


class ResidentialComplex(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images', blank=True)
    property = models.ForeignKey('apps.Property', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image for {self.property.name}"


class Tariff(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=Property.Status.choices, default=Property.Status.ACTIVE)
    label = models.CharField(max_length=10, choices=Property.Label.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('apps.User', on_delete=models.CASCADE, related_name='tariffs', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.price} UZS for {self.duration_days} days"


class StaticPage(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Metro(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    country = models.ForeignKey('apps.Country', on_delete=models.CASCADE, related_name='regions')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    region = models.ForeignKey('apps.Region', on_delete=models.CASCADE, related_name='cities')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    city = models.ForeignKey('apps.City', on_delete=models.CASCADE, related_name='districts')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

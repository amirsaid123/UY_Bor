from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models import CASCADE, CharField, ImageField, EmailField, DecimalField, DateTimeField, BooleanField, \
    TextChoices, Model, SlugField, ForeignKey, TextField, URLField, PositiveIntegerField, ManyToManyField, DateField, \
    IntegerField
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
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    phone_number = CharField(max_length=15, unique=True)
    avatar = ImageField(upload_to='avatars', blank=True)
    organization = CharField(max_length=255, blank=True)
    email = EmailField(unique=True, blank=True, null=True)
    balance = DecimalField(max_digits=10, decimal_places=2, default=0)
    role = CharField(max_length=255, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_active = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number


class Property(Model):
    class Material(TextChoices):
        BRICK = 'brick', 'Brick'
        MONOLITHIC = 'monolithic', 'Monolithic'
        CONCRETE_BLOCKS = 'concrete_blocks', 'Concrete Blocks'
        CONCRETE = 'concrete', 'Concrete'
        ANOTHER = 'another', 'Another'

    class Renovation(TextChoices):
        AUTHOR = 'author', 'Author design'
        EURO = 'euro', 'Euro renovation'
        MID = 'mid', 'Medium renovation'
        REQUIRED = 'required', 'Needs renovation'
        BLACK_PLASTER = 'black_plaster', 'Bare walls (Black plaster)'

    class Type(TextChoices):
        SALE = 'sale', 'Sale'
        RENT = 'rent', 'Rent'

    class Label(TextChoices):
        VIP = 'vip', 'VIP'
        PREMIUM = 'premium', 'Premium'
        URGENT = 'urgent', 'Urgent'

    class ResidentialType(TextChoices):
        FREE_LAYOUT = 'free_layout', 'Free layout'
        ON_TIME = 'on_time', 'On time'
        FINISHED = 'finished', 'Finished'

    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        MODERATION = 'moderation', 'Moderation'
        CANCELED = 'canceled', 'Canceled'

    name = CharField(max_length=255)
    address = CharField(max_length=255)
    building_material = CharField(max_length=100, choices=Material.choices)
    renovation_needed = CharField(max_length=100, choices=Renovation.choices)
    area = DecimalField(max_digits=10, decimal_places=2)
    room = PositiveIntegerField()
    floor = PositiveIntegerField()
    price = DecimalField(max_digits=10, decimal_places=0)
    description = TextField(null=True, blank=True)
    amenities = ManyToManyField('apps.Amenity', related_name='properties', blank=True)
    type = CharField(max_length=10, choices=Type.choices)
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='properties')
    label = CharField(max_length=10, choices=Label.choices, null=True, blank=True)

    residential_complex = ForeignKey('apps.ResidentialComplex', on_delete=CASCADE, null=True, blank=True)
    residential_type = CharField(max_length=100, choices=ResidentialType.choices, null=True, blank=True)
    commissioning_date = DateField(null=True, blank=True)

    views = IntegerField(default=0)
    saves = IntegerField(default=0)

    city = ForeignKey('apps.City', on_delete=CASCADE, related_name='properties')
    region = ForeignKey('apps.Region', on_delete=CASCADE, related_name='properties')
    metro = ForeignKey('apps.Metro', on_delete=CASCADE, related_name='properties', null=True, blank=True)
    district = ForeignKey('apps.District', on_delete=CASCADE, related_name='properties', null=True,
                                 blank=True)
    country = ForeignKey('apps.Country', on_delete=CASCADE, related_name='properties', null=True,
                                blank=True)

    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='properties')

    latitude = DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    status = CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Wishlist(Model):
    property = ForeignKey('apps.Property', on_delete=CASCADE, related_name='wishlist')
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='wishlist')


class Message(Model):
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='messages')
    from_user = ForeignKey('apps.User', on_delete=CASCADE, related_name='sent_messages', null=True,
                                  blank=True)
    text = TextField()
    created_at = DateTimeField(auto_now_add=True)


class Transaction(Model):
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='transactions')
    amount = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)


class Blog(Model):
    title = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    description = TextField(null=True, blank=True)
    image = ImageField(upload_to='blogs', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Video(Model):
    video = URLField()
    property = ForeignKey('apps.Property', on_delete=CASCADE, related_name='videos')


class ResidentialComplex(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    description = TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Amenity(Model):
    name = CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(Model):
    name = CharField(max_length=100)
    slug = SlugField(unique=True, blank=True)
    parent = ForeignKey(
        'self',
        on_delete=CASCADE,
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


class Image(Model):
    image = ImageField(upload_to='images', blank=True)
    property = ForeignKey('apps.Property', on_delete=CASCADE, related_name='images')

    def __str__(self):
        return f"Image for {self.property.name}"


class Tariff(Model):
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    duration_days = PositiveIntegerField()
    description = TextField(blank=True, null=True)
    status = CharField(max_length=10, choices=Property.Status.choices, default=Property.Status.ACTIVE)
    label = CharField(max_length=10, choices=Property.Label.choices, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price} UZS for {self.duration_days} days"

class StaticPage(Model):
    title = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    content = TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Metro(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Country(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Region(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    country = ForeignKey('apps.Country', on_delete=CASCADE, related_name='regions')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class City(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    region = ForeignKey('apps.Region', on_delete=CASCADE, related_name='cities')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    city = ForeignKey('apps.City', on_delete=CASCADE, related_name='districts')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

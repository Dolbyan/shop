from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import S3Client


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, unique=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    @classmethod
    def add_new_user(cls, name, email, password, is_staff=False):
        user = cls(name=name, email=email, is_staff=is_staff)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        app_label = "app"


class Items(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    price = models.IntegerField()
    amount = models.IntegerField()
    image = models.CharField(max_length=200, blank=True, null=True)
    image_name = models.CharField(max_length=200, null=True)

    @classmethod
    def get_inv(cls):

        s3 = S3Client()
        x = cls.objects.all()
        result = []
        for row in x:
            image_url = s3.get_file_url(row.image_name)
            if image_url:
                result.append((row, image_url))
        return result

    class Meta:
        db_table = "Items"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField("Items", related_name="order_item")
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    payment_status = models.BooleanField(default=False)


class Carts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Items', on_delete=models.CASCADE, related_name='cart_products')
    quantity = models.PositiveIntegerField(default=1)

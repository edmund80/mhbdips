from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    image = models.ImageField(upload_to='images')
    name = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    featured = models.BooleanField(default=False)
    favorites = models.ManyToManyField(User, related_name='favorite_products', blank=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Shipper(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)


class OrderDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=50, null=False)
    address = models.TextField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(null=False)
    total_price = models.FloatField(null=False)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE, null=True, default=None)
    product_image = models.ImageField(upload_to='order_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.user:
            self.name = self.user.get_full_name()
            self.email = self.user.email
        super(OrderDetail, self).save(*args, **kwargs)



class Invoice(models.Model):
    date = models.DateField()
    invoice_number = models.IntegerField()
    payee = models.CharField(max_length=50)
    due_date = models.DateField()
    amount_due = models.FloatField()
    paid_date = models.DateField()


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]
    contact_method = models.CharField(max_length=5, choices=CONTACT_METHOD_CHOICES)
    BEST_TIME_CHOICES = [
        ('am', 'AM'),
        ('pm', 'PM'),
    ]
    best_time = models.CharField(max_length=2, choices=BEST_TIME_CHOICES)
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

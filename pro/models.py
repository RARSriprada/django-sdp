from django.contrib.auth.models import AbstractUser
from django.db import models

class Book(models.Model):
    objects = None
    title = models.CharField(max_length=100, default='')
    author = models.CharField(max_length=100, default='')
    genre = models.CharField(max_length=100, default='')
    description = models.TextField(default='')  # Provide a default value
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    availability = models.CharField(max_length=20, default='available')
    image = models.ImageField(upload_to='book_images/', default='')

    def __str__(self):
        return self.title

class Order(models.Model):
    order_number = models.CharField(max_length=20, default='')
    books = models.ManyToManyField(Book)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.order_number

class Customer(models.Model):
    username = models.CharField(max_length=50, default='')
    email = models.CharField(max_length=50, default='')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

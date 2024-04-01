
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Customer(AbstractUser):
    address= models.CharField(max_length=100, null=False)



class Product(models.Model) :
    product = models.CharField(max_length=100, null=False)
    price = models.IntegerField(null=False)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)



class Order(models.Model): 
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)

    @property
    def get_total_price(self):
        return sum([item.get_total for item in  self.orderitem_set.all()])



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.IntegerField(default = 0)

    @property
    def get_total(self):
        return self.quantity * self.product.price
    


class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
 
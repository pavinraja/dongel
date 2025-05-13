from django.db import models

class user(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phonenumber = models.CharField(max_length=10)
    email = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.username

class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    picture = models.URLField(max_length=50000, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:A" \
    "Nd9GcRyqZKrn93kqP7pavGneBlqLFVJCRYZQMihKw&s")
    cuisine = models.CharField(max_length=40, default="Indian and Western")
    rating = models.CharField()

    def __str__(self):
        return self.name
    
class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=50)
    price = models.IntegerField()
    veg = models.BooleanField(default=False)
    picture = models.URLField(max_length=50000, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQE" \
    "KbRnx1UeLsXv3dZRMqGUgdBY2-AbpKuBA&s")


    def __str__(self):
        return self.name
    
class Cart(models.Model):
    customer = models.ForeignKey(user, on_delete=models.CASCADE, related_name="cart")
    def total_price(self):
        return sum(item.item.price * item.quantity for item in self.cart_items.all())

    def __str__(self):
        return f"{self.customer.username} : {self.total_price()}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"


 

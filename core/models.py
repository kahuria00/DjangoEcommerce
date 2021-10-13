from django.db import models
from django.conf import settings
from django.urls import reverse

category_choices=(
    ('V','vegetables'),
    ('F','Fruits'),
    ('C','Cereals'),
)
label_display_choices=(
    ('I','danger'),
    ('KG','primary'),
    ('B','success'),
)
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    category = models.CharField(choices=category_choices,max_length=1)
    label = models.CharField(choices=label_display_choices,max_length=1)
    slug = models.SlugField(default=None)
    description = models.TextField()
    image = models.ImageField()
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("core:product",kwargs={
            'slug': self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart",kwargs={
            'slug':self.slug
        })
    

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE)
    ordered =models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=(models.CASCADE))
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity}of{self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateField(auto_now_add=True)
    order_date = models.DateField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    current_stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class LineItem(models.Model):
    basket = models.ForeignKey(
        'Basket', related_name="lines",
        on_delete=models.CASCADE)

    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField()
    total = models.IntegerField()

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def save(self, *args, **kwargs):
        self.total = self.get_total_item_price()
        super(LineItem, self).save(*args, **kwargs)
        self.basket.save()

    def get_final_price(self):
        return self.get_total_item_price()


class Basket(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name="basket")
    total = models.PositiveIntegerField(default=0)

    def total_price(self):
        total = 0
        for line in self.lines.all():
            total += line.total
        return total

    @property
    def count_item(self):
        return self.lines.count()

    class Meta:
        verbose_name = 'Basket'

    def save(self, *args, **kwargs):
        self.total = self.total_price()
        super(Basket, self).save(*args, **kwargs)


class OrderLine(models.Model):
    order = models.ForeignKey(
        'Order', related_name="lines",
        on_delete=models.CASCADE)

    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    total = models.PositiveIntegerField()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=1)

    billing_address = models.ForeignKey(
        'Address', related_name='user_address', on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def product_id(self):
        return f"#YNT-{self.id}"


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Address'

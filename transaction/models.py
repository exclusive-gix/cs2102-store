from django.db import models, connection
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from .managers import CartManager

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    objects = CartManager()

    class Meta:
        managed = False
        db_table = 'cart'

    def __str__(self):
        shopping_list = "Total Quantity: {}".format(self.cartitem_set.aggregate(Count('id'))['id__count'])
        return "{} - ({})".format(self.buyer.username, shopping_list)

    def insert(self):
        with connection.cursor() as c:
            c.execute('''
                INSERT INTO cart(buyer_id)
                VALUES (%s)
            ''', [self.buyer_id])

class CartItem(models.Model):

    multimedia = (
        models.Q(app_label='multimedia', model = 'Book') |
        models.Q(app_label='multimedia', model = 'Movie') |
        models.Q(app_label='multimedia', model = 'Application') |
        models.Q(app_label='multimedia', model = 'Music') |
        models.Q(app_label='multimedia', model = 'Album'))

    cart = models.ForeignKey('Cart')
    content_type = models.ForeignKey(ContentType, limit_choices_to=multimedia)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    class Meta:
        db_table = 'cart_item'

    def __str__(self):
        return str(self.content_object)


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey('Cart')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'transaction'

    def __str__(self):
        return self.cart

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db import connection
from django.contrib.contenttypes.models import ContentType

from multimedia.utils import dictfetchone

from .models import (
    CartItem, 
    Cart,
)

from multimedia.models import Multimedia

def cart_item_list(request):
    cart_id = __getUserCartId(request.user.id)

    if cart_id == -1:
        newCart = Cart(buyer=request.user)
        newCart.insert()
        cart_id = __getUserCartId(request.user.id)

    cart_items_raw = CartItem.objects.raw("""SELECT ci.id, ci.object_id, m.name, m.price
                                             FROM cart_item ci, multimedia m 
                                             WHERE ci.object_id = m.id AND
                                                   ci.cart_id = %s
                                         """, [cart_id])

    total_price_raw = CartItem.objects.raw("""SELECT ci.id, sum(m.price) as total
                                              FROM cart_item ci, multimedia m 
                                              WHERE ci.object_id = m.id AND
                                                    ci.cart_id = %s
                                           """, [cart_id])

    cart_items = []
    total_price = 0

    for entry in total_price_raw:
        total_price = entry.total

    for cart_item in cart_items_raw:
        item = {}
        item['id'] = cart_item.object_id
        item['name'] = cart_item.name
        item['price'] = cart_item.price
        cart_items.append(item)

    return render(request, 'transaction/checkout.html', {'cart_id': cart_id, 'cart_items': cart_items, 'total_price': total_price})

def cart_purchase(request):
    cart_id = request.POST['cart_id']
    user = request.user

    __updateStatus(cart_id)

    newCart = Cart(buyer=user)
    newCart.insert()

    new_cart_id = __getUserCartId(user.id)

    return redirect("carts:cart_item_list")

def cart_item_delete(request):
    cart_id = request.POST['cart_id']
    cart_item_id = request.POST['cart_item_id']

    __deleteItem(cart_id, cart_item_id)

    return redirect("carts:cart_item_list")

def cart_item_add(request, multimedia_id, multimedia_type):
    user_id = request.user.id

    __addItem(user_id, multimedia_id, multimedia_type)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def __getUserCartId(user_id):
    cart_raw = Cart.objects.raw("""SELECT c1.id
                                   FROM cart c1
                                   WHERE c1.buyer_id = %s AND
                                         c1.is_completed = false AND
                                         c1.created_at >= ALL (SELECT c2.created_at FROM cart c2);
                                """, [user_id])

    result = sum(1 for row in cart_raw)

    new_cart_id = 0

    if result == 0:
        new_cart_id = -1
    elif result == 1:
        new_cart_id = cart_raw[0].id

    return new_cart_id

def __updateStatus(cart_id):
    with connection.cursor() as c:
        c.execute('''
            UPDATE cart
            SET is_completed = true
            WHERE id = %s
        ''', [cart_id])

def __deleteItem(cart_id, cart_item_id):
    with connection.cursor() as c:
        c.execute('''DELETE FROM cart_item 
                     WHERE cart_id = %s AND 
                           object_id = %s
        ''', [cart_id, cart_item_id])

def __addItem(user_id, multimedia_id, multimedia_type):
    content_type = ContentType.objects.get(model=multimedia_type)
    cart_id = __getUserCartId(user_id)
    if cart_id == -1:
        newCart = Cart(buyer_id=user_id)
        newCart.insert()
        cart_id = __getUserCartId(user_id)
    with connection.cursor() as c:
        c.execute('''INSERT INTO cart_item(cart_id, object_id, content_type_id) 
                     VALUES (%s, %s, %s)
        ''', [cart_id, multimedia_id, content_type.id])

def hasItemInCart(user_id, multimedia_id):
    cart_id = __getUserCartId(user_id)

    cart_item_raw = Cart.objects.raw("""SELECT ci.id 
                                        FROM cart_item ci
                                        WHERE cart_id = %s AND
                                              object_id = %s
                                     """, [cart_id, multimedia_id])

    result = sum(1 for row in cart_item_raw)

    return not result

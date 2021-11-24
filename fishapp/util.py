from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image
from django.db import models


def paginate(objects, size, request, context, var_name='object_list'):
    """Paginate objects provided by view.

    This function takes:
      * list of elements;
      * number of objects per page;
      * request object to get url parameters from;
      * context to set new variables into;
      * var_name - variable name for list of objects.

    It returns updated context object.
    """
    # apply pagination
    paginator = Paginator(objects, size)

    # try to get page number from request
    page = request.GET.get('page', '1')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        object_list = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999),
        # deliver last page of results
        object_list = paginator.page(paginator.num_pages)

    # set variables into context
    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator

    return context


def get_current_seen_products(request):
    """Returns currently seen products or None"""

    # we remember selected group in a cookie
    seen_products_ids = str(request.COOKIES.get('seen_products'))
    if seen_products_ids != 'None' and seen_products_ids:
        seen_products_ids = seen_products_ids.split('%2C')

    if seen_products_ids != 'None' and seen_products_ids:
        from .models import Product
        try:
            seen_products = Product.objects.filter(id__in=seen_products_ids)
        except Product.DoesNotExist:
            return None
        else:
            return seen_products
    else:
        return None


def recalc_cart(cart):
    # "звернись до всіх продуктів і порахуй у всіх загальну final_price"
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Sum('qty'))  # SQL ф-я інтерпрет. Джангою

    # models.Count('id') - Порахує всі товар в корзині

    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data.get('final_price__sum')
    else:
        cart.final_price = 0

    if cart_data.get('qty__sum'):
        cart.total_products = cart_data.get('qty__sum')
    else:
        cart.total_products = 0
    # self.total_products = cart_data['id__count']  # Поверни к-сть товару
    # print(cart_data)  # {'final_price__sum': None, 'id__count': 0}

    cart.save()  # Зберегти

import random

# from dbtunnel import start_tunnel, stop_tunnel
from django.db.models import Q
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import SingleObjectMixin, ContextMixin
from django.views.generic import View, TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .models import Category, Customer, Cart, Product, CartProduct, Order, SubCategory
from .util import get_current_seen_products, paginate


slg = None
s_categories = None
ctgories = None
seen_products = None
prods = {}
crt = None
srch_count = None


class SidebarMixin(View):

    def dispatch(self, request, *args, **kwargs):

        search = str(request.GET.get('search_input', ''))

        slug = kwargs.get('slug')
        category = Category.annotate_objects.get_categories_for_left_sidebar().filter(slug=slug).first()
        categories = Category.annotate_objects.get_categories_for_left_sidebar().all()

        if category:
            sub_categories = SubCategory.annotate_objects.get_categories_for_left_sidebar().filter(category=category.id)
        else:
            sub_categories = SubCategory.annotate_objects.get_categories_for_left_sidebar().filter(
                category__name='Not_Existing_____________')

        self.slug = slug
        self.sub_categories = sub_categories
        self.categories = categories

        global slg, s_categories, ctgories, seen_products, prods, srch_count

        slg = slug
        s_categories = sub_categories
        ctgories = categories

        if kwargs.get('sub_slug'):
            products = Product.objects.filter(
                sub_category=self.sub_categories.filter(sub_slug=kwargs.get('sub_slug')).first()
            )
        else:
            products = Product.objects.filter(
                category=self.categories.filter(slug=kwargs.get('slug')).first()
            ).filter(sub_category=None)

        if search:
            products = Product.objects.filter(
                Q(title__icontains=search) | Q(code__icontains=search)
            )

            srch_count = products.count()

        try:
            if get_current_seen_products(request):
                seen_products = get_current_seen_products(request)
        except AttributeError:
            pass

        order_by = request.GET.get('order_by')
        if order_by in ('price', 'price1', 'title', 'created1'):
            if '1' not in order_by:
                products = products.order_by(f'{order_by}')
            else:
                products = products.order_by(f'-{order_by[:-1]}')

        max_ = request.GET.get('max')
        min_ = request.GET.get('min')
        if min_ and max_:
            products = products.filter(price__gte=int(min_)).filter(price__lte=int(max_))

        self.products = products

        # Paginate
        on_page = request.GET.get('on_page')
        self.on_page = on_page

        if on_page:
            paginate(products, int(on_page), request, prods, 'products')
        else:
            paginate(products, 24, request, prods, 'products')

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        page = request.POST.get('page')
        posts = self.products
        # use Django's pagination
        # https://docs.djangoproject.com/en/dev/topics/pagination/
        user = request.user

        if self.on_page:
            results_per_page = int(self.on_page)
        else:
            results_per_page = 24

        paginator = Paginator(posts, results_per_page)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(2)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        # build a html posts list with the paginated posts
        posts_html = loader.render_to_string(
            'include/posts.html',
            {'posts': posts,
             'user': user}
        )
        # package output data and return it as a JSON object
        output_data = {
            'posts_html': posts_html,
            'has_next': posts.has_next()
        }
        return JsonResponse(output_data)


class CartMixin(View):  # View + dispatch = добрались до юзера і написали міксин

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:  # якщо користувач авторизований

            customer = Customer.objects.filter(user=request.user).first()  # шукаємо його (може бти юзер но не кастомер)

            if not customer:  # Для зареєстрованого но без кастомера (екстра-перевірка)
                customer = Customer.objects.create(
                    user=request.user
                )
            # шукаємо кошик цього користувача, який не є в заказі
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)  # Якщо не створений - створ

        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()

            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)

        global crt
        self.cart = cart  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        crt = cart
        # self.cart.save()
        return super().dispatch(request, *args, **kwargs)


class SidebarContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()

        if srch_count:
            context['search_count'] = srch_count
        if slg:
            context["slug"] = slg
        if s_categories:
            context["sub_categories"] = s_categories
        if ctgories:
            context["categories"] = ctgories
        if crt:
            context["cart"] = crt

        # Sidebar Group --------
        seen_categories_list = list()
        randomized_seen_products = list()
        if seen_products:
            context["seen_products"] = seen_products
            randomized_seen_products = random.sample(list(context["seen_products"]), len(context["seen_products"]))
            for seen_product in context["seen_products"]:
                seen_categories_list.append(seen_product.category)

        new_products_not_shuffled = all_products.order_by('created')[:int(all_products.count())/100*50:10]
        new_products = random.sample(new_products_not_shuffled, len(new_products_not_shuffled))

        top_sale_products = all_products.filter(sold__gt=0).order_by('-sold')

        context["sidebar"] = []
        if randomized_seen_products:
            context["sidebar"].append(("Ви переглядали", randomized_seen_products))
            context["seen_products"] = seen_products

        if top_sale_products:
            context["sidebar"].append(("Топ продаж", random.sample(list(top_sale_products), len(top_sale_products))))
            context["top_sale_products"] = top_sale_products

        if new_products:
            context["sidebar"].append(("Новинки", new_products))
            context["new_products"] = new_products

        # Recommend Group --------
        may_interest = ''
        if seen_products:
            may_interest = all_products.exclude(id__in=context["seen_products"]).filter(category__in=seen_categories_list)
        # hot_discounts = all_products.filter(discount__gt=19)
        new_products_recommend = random.sample(list(new_products), len(new_products))[:8]

        context["recommend"] = []
        if may_interest:
            context["recommend"].append(("Можуть зацікавити", random.sample(list(may_interest), len(may_interest))[:8]))

        # if hot_discounts:
        #     context["recommend"].append(("Гарячі знижки", random.sample(list(hot_discounts), len(hot_discounts))[:8]))

        if new_products_recommend:
            context["recommend"].append(("Новинки", new_products_recommend))

        context['top_seen'] = ['Топ продаж', 'Ви переглядали']

        if prods:
            for key, val in prods.items():
                context[f"{key}"] = val

        return context


class AJAXResponseMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            return JsonResponse({'status': 'OK', 'prod_id': kwargs.get('pk')})
        return super().dispatch(request, *args, **kwargs)


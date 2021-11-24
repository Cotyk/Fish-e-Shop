from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render

# from fishapp import db_mysql
from django.views import View
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView

from django.contrib import messages
from django.contrib.auth import authenticate, login

from fishapp.models import Product, CartProduct, Cart, Customer, Order
from fishapp.mixins import SidebarMixin, AJAXResponseMixin, SidebarContextMixin, CartMixin
from .util import recalc_cart
from .forms import LoginForm, RegisterForm
from django.utils.safestring import mark_safe


def test_view(request):
    # print('0000000000000))))))))))))))))))))))))')
    # ssh_pg_connect()
    # db_mysql.all_users()
    # obj = Category.objects.all()
    # print(obj)
    print()
    print('SENDING EMAIL ..... START')
    send_mail(
        fail_silently=False,
        subject='ReligionPeace Live (Статус платежу)',
        message=None,
        html_message='<h1>Hello from Valiunya</h1>',
        from_email='valiunyavovchak@gmail.com',
        recipient_list=['valentyn.vovchak@gmail.com']
    )
    print('SENDING EMAIL ..... END')

    return render(request, 'fishapp/test.html', {})


class BaseView(SidebarMixin, CartMixin, SidebarContextMixin, TemplateView):

    template_name = 'fishapp/base.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Щоб додавати товар у кошик, Вам необхідно увійти.')

        return super().dispatch(request, *args, **kwargs)


class CategoryView(SidebarMixin, SidebarContextMixin, CartMixin, TemplateView):

    template_name = 'fishapp/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["current_category"] = self.categories.filter(slug=kwargs.get('slug')).first()
        # products = Product.objects.filter(category=context["current_category"]).filter(sub_category=None)
        # context["products"] = products
        return context


class CatalogView(SidebarMixin, CartMixin, SidebarContextMixin, TemplateView):

    template_name = 'fishapp/catalog.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.GET.get('page', ''):
            self.template_name = 'fishapp/404.html'

        return super(CatalogView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context["current_category"] = self.categories.filter(slug=kwargs.get('slug')).first()
        except AttributeError:
            pass

        try:
            current_subcategory = self.sub_categories.filter(sub_slug=kwargs.get('sub_slug')).first()
            context["current_subcategory"] = current_subcategory
        except AttributeError:
            pass

        if self.request.GET.get('search_input'):
            context['srch_count'] = '1'

        # products = Product.objects.filter(sub_category=current_subcategory).order_by('image')
        # context["products"] = products
        return context


class ProductDetailView(SidebarMixin, CartMixin, SidebarContextMixin, AJAXResponseMixin, TemplateView):

    template_name = 'fishapp/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = Product.objects.get(pk=kwargs.get('pk'))
        context["current_category"] = self.categories.filter(slug=kwargs.get('slug')).first()
        current_subcategory = self.sub_categories.filter(sub_slug=kwargs.get('sub_slug')).first()
        if current_subcategory:
            context["current_subcategory"] = current_subcategory

        if context["product"].description:
            context['html_description'] = mark_safe('<p>'+context["product"].description+'</p>')
        else:
            context['html_description'] = mark_safe('<p></p>')

        if context["product"] in [cp.product for cp in self.cart.products.all()]:
            context["in_cart"] = "1"

        return context


class CartView(SidebarMixin, CartMixin, SidebarContextMixin, TemplateView):
    template_name = "fishapp/cart.html"

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)

        context['crt'] = '1'
        return context


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        slug, sub_slug, pk = kwargs.get('slug'), kwargs.get('sub_slug'), kwargs.get('pk')

        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer, in_order=False)
        product = Product.objects.get(pk=pk)

        cart_product, created = CartProduct.objects.get_or_create(
            user=customer,
            cart=cart,
            product=product
        )
        if created:
            cart.products.add(cart_product)

        recalc_cart(self.cart)  # кошик оновлюється тільки коли в нього щось додається
        messages.add_message(request, messages.SUCCESS, "Товар успішно доданий")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        slug, sub_slug, pk = kwargs.get('slug'), kwargs.get('sub_slug'), kwargs.get('pk')

        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer, in_order=False)
        product = Product.objects.get(pk=pk)

        cart_product = CartProduct.objects.get(
            user=customer,
            cart=cart,
            product=product
        )

        self.cart.products.remove(cart_product)  # Видаляємо з кошика
        cart_product.delete()  # Видаляємо той CartProduct
        # self.cart.save()  # кошик оновлюється тільки коли в нього щось додається
        recalc_cart(self.cart)
        messages.add_message(request, messages.SUCCESS, "Товар успішно видалений")
        return HttpResponseRedirect('/cart/')

        # context --------------------> CartProduct.get_model_name()


class ChangeQTYView(CartMixin, TemplateView):
    template_name = 'fishapp/cart.html'

    def post(self, request, *args, **kwargs):
        dat = request.POST
        value = dat["value"]

        pk = kwargs.get('pk')
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer, in_order=False)
        product = Product.objects.get(pk=pk)

        cart_product = CartProduct.objects.get(
            user=customer,
            cart=cart,
            product=product
        )

        cart_product.qty = value
        cart_product.save()
        # self.cart.save()
        recalc_cart(self.cart)
        # messages.add_message(request, messages.INFO, "К-сть успішно змінено")
        return JsonResponse({'key': 'success'})


errors = None
data = None


class CheckoutView(SidebarMixin, CartMixin, SidebarContextMixin, TemplateView):
    # В нас кошик прив'язаний до клієнта. Щоб отимати кошик даного клієнта, треба отримати цього клієта.
    template_name = 'fishapp/checkout.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)

        context["checkout"] = '1'
        if errors:
            context["errors"] = errors

        if data:
            context["data"] = data

        return context


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)

        # errors collection
        global errors, data
        errors = {}

        # data for order object
        data = {'comment': request.POST.get('comment'), 'customer': customer}

        # validate user input
        phone = request.POST.get('phone', '').strip()
        if not phone:
            errors['phone'] = "Номер телефону є обов'язковим"
        else:
            data['phone'] = phone

        buying_type = request.POST.get('buying_type', '').strip()
        if not buying_type:
            errors['buying_type'] = "Спосіб доставки є обов'язковим"
        else:
            section = request.POST.get('section', '').strip()
            if not section and str(buying_type) == 'delivery':
                errors['section'] = "Ви запросили доставку у відділення, це поле є обов'язковим"
            else:
                data['section'] = section

            data['buying_type'] = buying_type

        paying_type = request.POST.get('paying_type', '').strip()
        if not paying_type:
            errors['paying_type'] = "Спосіб оплати є обов'язковим"
        else:
            data['paying_type'] = paying_type

        address = request.POST.get('address', '').strip()
        if not address:
            errors['address'] = "Адрес є обов'язковим"
        else:
            data['address'] = address

        first_name = request.POST.get('first_name', '').strip()
        if not first_name:
            errors['first_name'] = "Ім'я є обов'язковим"
        else:
            data['first_name'] = first_name

        last_name = request.POST.get('last_name', '').strip()
        if not last_name:
            errors['last_name'] = "Прізвище є обов'язковим"
        else:
            data['last_name'] = last_name

        region = request.POST.get('region', '').strip()
        if not region:
            errors['region'] = "Область є обов'язковою"
        else:
            data['region'] = region

        location = request.POST.get('location', '').strip()
        if not location:
            errors['location'] = "Населений пункт є обов'язковим"
        else:
            data['location'] = location

        # save order
        if not errors:
            new_order = Order(**data)
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()

            customer.orders.add(new_order)
            messages.add_message(request, messages.SUCCESS, 'Дякуємо за замовлення! Незабаром з Вами зв\'яжемося.')

            # products in this cart were sold
            for cart_product in self.cart.products.all():
                # recalculate sold fields
                for i in range(cart_product.qty):
                    cart_product.product.sold += 1
                cart_product.product.save()

            # redirect to homepage
            return HttpResponseRedirect(reverse('homepage'))

        else:
            # render form with errors and previous user input
            # return render(request, 'fishapp/checkout.html', {'errors': errors})
            messages.add_message(request, messages.ERROR, 'Будь ласка, виправте наступні помилки:')
            return HttpResponseRedirect(reverse('checkout'))

        # if form.is_valid():
        #     new_order = form.save(commit=False)
        #
        #     new_order.customer = customer
        #     new_order.first_name = form.cleaned_data["first_name"]
        #     new_order.last_name = form.cleaned_data["last_name"]
        #     new_order.phone = form.cleaned_data["phone"]
        #     new_order.address = form.cleaned_data["address"]
        #     new_order.buying_type = form.cleaned_data["buying_type"]
        #     new_order.comment = form.cleaned_data["comment"]
        #     new_order.save()
        #
        #     self.cart.in_order = True
        #     self.cart.save()
        #     new_order.cart = self.cart
        #     new_order.save()
        #
        #     customer.orders.add(new_order)
        #     messages.add_message(request, messages.INFO, 'Дякуємо за замовлення! Незабаром з Вами зв\'яжемося.')
        #
        #     return HttpResponseRedirect(reverse('homepage'))
        #
        # return HttpResponseRedirect(reverse('checkout'))


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'fishapp/auth/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if user.first_name:
                    messages.add_message(request, messages.SUCCESS, f'Вітаємо, {user.first_name}! Авторизація пройшла успішно!')
                else:
                    messages.add_message(request, messages.SUCCESS, f'Вітаємо, {user.username}! Авторизація пройшла успішно!')

                messages.add_message(request, messages.INFO, f'Для користувачів, які мають пластикову картку від borntofish - знижка 5% на УСІ товари. А оформлюючи замовлення, вартість якого перевищує 300 грн, власники картки отримують знижку 10%.')

                return HttpResponseRedirect('/')

        else:
            return render(request, 'fishapp/auth/login.html', {'form': form, 'cart': self.cart})


class RegisterView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'fishapp/auth/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username, email, password)
            if user:

                if user.first_name:
                    messages.add_message(request, messages.SUCCESS, f'Вітаємо, {user.first_name}! Ви успішно зареєстрували новий акаунт. Увійдіть.')
                else:
                    messages.add_message(request, messages.SUCCESS, f'Вітаємо, {user.username}! Ви успішно зареєстрували новий акаунт. Увійдіть.')

                # messages.add_message(request, messages.INFO, f'Для користувачів, які мають пластикову картку від borntofish - знижка 5% на УСІ товари. А оформлюючи замовлення, вартість якого перевищує 300 грн, власники картки отримують знижку 10%.')

                return HttpResponseRedirect(reverse('login'))

        else:
            return render(request, 'fishapp/auth/register.html', {'form': form, 'cart': self.cart})

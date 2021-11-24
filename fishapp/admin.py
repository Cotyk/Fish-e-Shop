from PIL import Image

from django.forms import ModelChoiceField, ModelForm, ValidationError

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, JsonResponse

from django.urls import resolve, reverse
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Product, Category, Cart, CartProduct, Customer, Order, SubCategory, Images
from django.core.exceptions import ObjectDoesNotExist

category_for_update = None


class ProductAdminForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def clean_category(self):
        data = self.cleaned_data['category']

        if category_for_update:
            self.fields['sub_category'].queryset = SubCategory.objects.filter(category=category_for_update)
            return data

        elif self.instance:
            try:
                self.fields['sub_category'].queryset = SubCategory.objects.filter(category=self.instance.category.id)
                return data
            except ObjectDoesNotExist:
                self.fields['sub_category'].queryset = SubCategory.objects.filter(sub_name='Not_Existing_____________')
                return data

        else:
            self.fields['sub_category'].queryset = SubCategory.objects.filter(sub_name='Not_Existing_____________')
            return data

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        try:
            self.fields['sub_category'].queryset = SubCategory.objects.filter(category=self.instance.category.id)
        except ObjectDoesNotExist as e:
            self.fields['sub_category'].queryset = SubCategory.objects.filter(sub_name='Not_Existing_____________')


class ProductImagesInline(admin.TabularInline):
    model = Images


class ProductAdmin(admin.ModelAdmin):

    form = ProductAdminForm
    change_form_template = 'admin/fishapp/product/add/change_form.html'
    search_fields = ('title', 'category__name', 'sub_category__sub_name')
    date_hierarchy = 'created'
    exclude = ['images']
    list_filter = ('category', 'sub_category')
    list_editable = ['remaining']
    list_display = ('title', 'category', 'sub_category', 'remaining', 'sold', 'image_tags')
    readonly_fields = ['image_tags']  # Be sure to read only mode
    inlines = [
        ProductImagesInline,
    ]  # Дати можливість добавляти в одну лінію багато фото товару

    # fields = ('avatar_tag', 'user')  # Specify the fields that need to be displayed in the administrative form

    def view_on_site(self, obj):
        if obj.sub_category:
            return reverse('product', args=[obj.category.slug, obj.sub_category.sub_slug, obj.id])
        else:
            return reverse('product', args=[obj.category.slug, obj.id])


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'image_tag')
    readonly_fields = ['image_tag']


class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ('sub_name',)
    list_display = ('sub_name', 'category', 'image_tag')
    readonly_fields = ['image_tag']
    list_filter = ('category',)


class CartProductAdmin(admin.ModelAdmin):
    search_fields = ('cart__id', )
    list_display = ('product', 'qty', 'user', 'cart')
    list_filter = ('cart',)


class OrderAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if obj:
            order_products = obj.cart.products.all()

            self.fieldsets[1][1]["description"] = f'<table style="border-collapse: collapse;margin: 25px 0;font-size: 1.5em;font-family: sans-serif;min-width: 400px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);"><thead><tr><th>Назва</th><th>Категорія</th><th>Підкатегорія</th><th>Артикул borntofish</th><th>Ціна / шт</th><th>К-сть</th><th>Загальна ціна, UAH</th><th>Залишок на складі</th></tr></thead><tbody>'
            if order_products:
                for order_product in order_products:
                    self.fieldsets[1][1]["description"] += f"""<tr><td>{order_product.product.title}</td><td>{order_product.product.category or '-'}</td><td>{order_product.product.sub_category or '-'}</td><td>{order_product.product.code}</td><td>{order_product.product.price or '-'}</td><td>{order_product.qty}</td><td>{order_product.final_price}</td><td>{order_product.product.remaining}</td></tr>"""
            else:
                self.fieldsets[1][1]["description"] += '<tr><td>Послуга не розщеплювалась</td></tr>'

            self.fieldsets[1][1]["description"] += '</tbody></table>'

            self.fieldsets[1][1]["description"] += f"""<div style="font-size: 15px; line-height: 1.8;">Усього товарів:  <span style="font-weight:bold;">{obj.cart.total_products}</span></div>"""
            self.fieldsets[1][1]["description"] += f"""<div style="font-size: 15px; line-height: 1.8;">Загальна ціна:  <span style="font-weight:bold;">{obj.cart.final_price} UAH</span></div>"""
            # form.base_fields['service'].widget.attrs["style"] = 'pointer-events: none;'
        return form

    search_fields = ('customer__user__last_name', 'customer__user__first_name', 'id')
    list_display = ('id', 'customer', 'cart', 'created_at', 'final__price', 'status')
    list_display_links = ['id', 'customer']
    readonly_fields = ['customer', 'first_name', 'last_name', 'phone', 'cart', 'comment', 'region', 'location',
                       'address', 'status', 'buying_type', 'paying_type', 'section']
    list_editable = ['status']
    list_filter = ('status',)
    date_hierarchy = 'created_at'

    fieldsets = [
        (None, {'fields': ('customer', 'first_name', 'last_name', 'phone', 'comment', 'region', 'location',
                           'address', 'status', 'buying_type', 'paying_type', 'section')}),
        ('Товари замовлення', {
            'fields': ('cart',),
            'description': '',
        }),
    ]

    def final__price(self, obj):
        return obj.cart.final_price

    final__price.short_description = 'Заг. ціна'
    final__price.admin_order_field = 'cart__final_price'


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ('user__first_name', 'user__last_name', 'user__id')
    list_display = ('__str__', 'address', 'phone', '_orders')

    def _orders(self, obj):
        return ", ".join([str(o) for o in obj.orders.all()])


class CartAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    list_display = ('__str__', 'owner', 'total_products', 'final_price', 'for_anonymous_user', 'in_order')
    list_filter = ('in_order', 'for_anonymous_user')


def update_json_field_view(request):
    # template_name = 'fishapp/templates/admin/fishapp/product/add/change_form.html'

    # def post(self, request, *args, **kwargs):
    if request.is_ajax():

        global category_for_update
        category_for_update = request.POST.get('id')

        return JsonResponse({'status': 'OK'})


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartProduct, CartProductAdmin)

# admin.site.register(Images)

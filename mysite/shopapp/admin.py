from django.contrib import admin
from django.db.models import QuerySet

from .models import Product, Order

from .admin_mixins import ExportCSVMixin


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportCSVMixin):
    actions = [mark_archived, mark_unarchived, 'export_csv']
    inlines = [OrderInline]
    list_display = ['pk', 'name', 'description_short', 'price', 'discount', 'archived']
    list_display_links = ['pk', 'name']
    ordering = ('pk',)
    search_fields = ('name', 'description',)
    fieldsets = [
        (None, {
            'fields': ('name', 'description', )
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('collapse', 'wide'),
        }),
        ('Extra options', {
            'fields': ('archived', ),
            'classes': ('collapse', '')
        })
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        else:
            return obj.description[:48] + '...'


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline
    ]
    list_display = ('delivery_address', 'promo_code', 'created_at', 'user_verbose')

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username



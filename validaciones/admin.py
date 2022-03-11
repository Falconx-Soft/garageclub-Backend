from django.contrib import admin
from .models import *

class ValidationAdmin(admin.ModelAdmin):
    list_display = ('reference', 'make', 'model','amount_purchase','amount_sale','margin','type','risk')

class VatAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount')

class CostAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount')

class CostQuantityAdmin(admin.ModelAdmin):
    list_display = ('quantity','cost')

class ProfitabilityAdmin(admin.ModelAdmin):
    list_display = ('min_purchase_range','max_purchase_range','typeA','typeB','typeC')

# Register your models here.
admin.site.register (Vat,VatAdmin)
admin.site.register (Cost,CostAdmin)
admin.site.register (CostQuantity,CostQuantityAdmin)
admin.site.register (Validation,ValidationAdmin)
admin.site.register (Profitability,ProfitabilityAdmin)


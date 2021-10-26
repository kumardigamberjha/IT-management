from django.contrib import admin
from django.db import models
from django.db.models import fields

from .models import Brand_Master, Category, Item_Master, Opening_Stock, Department, Issued_to, RequisitionForm, User_Master, IT_Purchase, Vendor_Master, item_condition, item_location, item_status, warranty_period, Order_Status, Purchase_Receiving
from import_export.admin import ImportExportModelAdmin

admin.site.register(User_Master)
@admin.register(IT_Purchase)
class IT_Purchase_Resources(ImportExportModelAdmin):
    pass
    class Meta:
        model = IT_Purchase
        fields = ['purchase_id', "date_of_purchase", "Vendor"]

admin.site.register(Opening_Stock)
admin.site.register(Issued_to)
admin.site.register(Purchase_Receiving)

admin.site.register(Department)
admin.site.register(item_condition)
admin.site.register(item_location)
admin.site.register(item_status)
admin.site.register(Item_Master)
admin.site.register(Brand_Master)
admin.site.register(warranty_period)
admin.site.register(Category)
@admin.register(RequisitionForm)
class RequisitionFormResources(admin.ModelAdmin):
    list_display = ["req_number", "req_Date", 'item', 'capacity', 'version','qty']
admin.site.register(Vendor_Master)
admin.site.register(Order_Status)


# clientdoc/admin.py

from django.contrib import admin
from .models import (
    Item, StoreLocation, SalesInvoice, InvoiceItem,
    DeliveryChallan, TransportCharges, ConfirmationDocument, PackedImage,
    OurCompanyProfile, Buyer, ItemCategory
)

# --- Inline Classes ---

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

class PackedImageInline(admin.TabularInline):
    model = PackedImage
    extra = 1

# --- Model Admin Registrations ---

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'gstin']
    search_fields = ['name', 'gstin']

@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'article_code', 'price', 'gst_rate']
    search_fields = ['name', 'article_code']
    list_filter = ['category']

@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'priority']
    search_fields = ['name', 'city', 'site_code']
    list_filter = ['state', 'priority']

@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'app_invoice_number', 'buyer', 'location', 'date', 'total', 'status']
    inlines = [InvoiceItemInline]
    list_filter = ['status', 'date']

@admin.register(DeliveryChallan)
class DeliveryChallanAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'date']

@admin.register(TransportCharges)
class TransportChargesAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'charges', 'date']

@admin.register(ConfirmationDocument)
class ConfirmationDocumentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'combined_pdf']
    inlines = [PackedImageInline]
    
@admin.register(OurCompanyProfile) 
class OurCompanyProfileAdmin(admin.ModelAdmin):
    # Restrict to only one entry
    def has_add_permission(self, request):
        return not OurCompanyProfile.objects.exists()

    list_display = ['name', 'gstin']
    fieldsets = (
        (None, {'fields': ('name', 'address', 'contact_number', 'email', 'signature')}),
        ('Tax Details', {'fields': ('gstin', 'state', 'state_code')}),
        ('Bank Details', {'fields': ('bank_name', 'account_holder_name', 'account_number', 'ifsc_code', 'branch_name')}),
    )
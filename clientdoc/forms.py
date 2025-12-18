from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset

from .models import (
    Item, StoreLocation, SalesInvoice, DeliveryChallan, TransportCharges,
    ConfirmationDocument, PackedImage, InvoiceItem, Buyer
)

# --- NEW FORMS ---

class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-0'),
                Column('gstin', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('address', css_class='form-group col-md-8 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                 Column('email', css_class='form-group col-md-6 mb-0'),
                 Column('phone', css_class='form-group col-md-6 mb-0'),
                 css_class='form-row'
            ),
            Submit('submit', 'Save Buyer', css_class='btn-primary mt-3')
        )

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('category', css_class='form-group col-md-4 mb-0'),
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('article_code', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('price', css_class='form-group col-md-3 mb-0'),
                Column('gst_rate', css_class='form-group col-md-3 mb-0'),
                Column('hsn_code', css_class='form-group col-md-3 mb-0'),
                Column('unit', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Item', css_class='btn-primary mt-3')
        )

# --- NEW INVOICE FORM (FIXES THE IMPORT ERROR) ---

class InvoiceForm(forms.ModelForm):
    """Form for editing the SalesInvoice header (location, date, and Tally Invoice No.)."""
    class Meta:
        model = SalesInvoice
        # Fields include the new tally_invoice_number field and other details
        fields = [
            'buyer', 'location', 'date', 'tally_invoice_number',
            'delivery_note', 'mode_terms_payment', 'reference_no_date', 'other_references',
            'buyers_order_no', 'buyers_order_date', 'dispatch_doc_no', 'delivery_note_date',
            'dispatched_through', 'destination', 'terms_of_delivery', 'remark'
        ] 
        widgets = {
            'date': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'buyers_order_date': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'delivery_note_date': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'terms_of_delivery': forms.Textarea(attrs={'rows': 3}),
            'remark': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Internal/Invoice Remarks'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['buyer'].required = False
        self.fields['buyer'].label = "Buyer (Bill To)"
        
        # Optional: Adds Crispy Form layout for better display if you are using it
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('buyer', css_class='form-group col-md-6 mb-0'),
                Column('location', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('date', css_class='form-group col-md-4 mb-0'),
                Column('tally_invoice_number', css_class='form-group col-md-4 mb-0'),
                Column('remark', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Fieldset(
                "Delivery & Payment Details",
                Row(
                    Column('delivery_note', css_class='form-group col-md-3 mb-0'),
                    Column('mode_terms_payment', css_class='form-group col-md-3 mb-0'),
                    Column('reference_no_date', css_class='form-group col-md-3 mb-0'),
                    Column('other_references', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'
                ),
                 Row(
                    Column('buyers_order_no', css_class='form-group col-md-3 mb-0'),
                    Column('buyers_order_date', css_class='form-group col-md-3 mb-0'),
                    Column('dispatch_doc_no', css_class='form-group col-md-3 mb-0'),
                    Column('delivery_note_date', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'
                ),
                 Row(
                    Column('dispatched_through', css_class='form-group col-md-4 mb-0'),
                    Column('destination', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                 Row(
                    Column('terms_of_delivery', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                )
            ),
            Submit('submit', 'Save Invoice Header', css_class='btn-primary mt-3')
        )

# --- EXISTING/STANDARD FORMS ---



class StoreLocationForm(forms.ModelForm):
    class Meta:
        model = StoreLocation
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
             Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('gstin', css_class='form-group col-md-3 mb-0'),
                Column('site_code', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('address', css_class='form-group col-md-8 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('state', css_class='form-group col-md-6 mb-0'),
                Column('state_code', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Location', css_class='btn-primary mt-3')
        )

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['item', 'quantity_shipped', 'quantity_billed', 'price', 'discount_type', 'discount_value', 'gst_rate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

InvoiceItemFormSet = inlineformset_factory(SalesInvoice, InvoiceItem, form=InvoiceItemForm, extra=1)

class DeliveryChallanForm(forms.ModelForm):
    class Meta:
        model = DeliveryChallan
        fields = ['date', 'notes']
        widgets = {
             'date': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

class TransportChargesForm(forms.ModelForm):
    class Meta:
        model = TransportCharges
        fields = ['date', 'charges', 'description']
        widgets = {
             'date': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

# --- CONFIRMATION DOCUMENT FORMS (UPDATED) ---

class ConfirmationDocumentForm(forms.ModelForm):
    """Form to handle the PO and Approval Email file uploads/replacement."""
    class Meta:
        model = ConfirmationDocument
        fields = ['po_file', 'approval_email_file']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['po_file'].required = False
        self.fields['approval_email_file'].required = False

class PackedImageForm(forms.ModelForm):
    """Form for individual PackedImage, including the new 'notes' field."""
    class Meta:
        model = PackedImage
        fields = ['image', 'notes'] # Added 'notes' field
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure image is not required by default widget validation to allow retaining existing file
        self.fields['image'].required = False 

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        notes = cleaned_data.get('notes')
        
        # If this is a new instance (no PK), and we have notes but no image -> Error
        if not self.instance.pk and not image and notes:
             # But wait, if user wants to delete? 
             # If no image, it's invalid for a PackedImage.
             self.add_error('image', 'Image is required for new entries.')
        elif not self.instance.pk and not image:
             # If empty form (no image, maybe no notes), FormSet handles deletion of empty forms?
             # But if Notes are present, form is "changed".
             pass
        return cleaned_data

# Updated formset to use the new PackedImageForm and enable deletion
PackedImageFormSet = inlineformset_factory(
    ConfirmationDocument, 
    PackedImage, 
    form=PackedImageForm, 
    extra=1, 
    can_delete=True
)
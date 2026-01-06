# clientdoc/urls.py

from django.urls import path
from . import views

app_name = 'clientdoc'

urlpatterns = [
    # 1. DASHBOARD (Root Path Fix)
    path('', views.dashboard, name='dashboard'), 
    
    # 2. NEW LIST VIEWS (Requested Features)
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('delivery-challans/', views.dc_list, name='dc_list'),
    path('transport-charges/', views.transport_list, name='transport_list'),
    path('confirmation-docs/', views.confirmation_list, name='confirmation_list'),
    path('bulk-upload/', views.bulk_upload_page, name='bulk_upload_page'),
    path('bulk-upload/sample/', views.download_sample_excel, name='download_sample_excel'),
    
    path('locations/<int:pk>/edit/', views.edit_location, name='edit_location'),
    path('locations/<int:pk>/', views.store_location_detail, name='store_location_detail'),
    path('buyers/', views.buyer_list, name='buyer_list'),
    path('buyers/new/', views.create_buyer, name='create_buyer'),
    path('buyers/<int:pk>/edit/', views.edit_buyer, name='edit_buyer'),
    path('buyers/<int:pk>/', views.buyer_detail, name='buyer_detail'),
    
    # 3. ITEM & LOCATION MANAGEMENT (Missing URLs Fixed)
    path('items/', views.item_list, name='item_list'),
    path('items/new/', views.create_item, name='create_item'),
    path('items/<int:pk>/edit/', views.edit_item, name='edit_item'),
    
    path('locations/', views.store_location_list, name='store_location_list'),
    path('locations/new/', views.create_location, name='create_location'),
    path('invoices/new/', views.create_invoice, name='create_invoice'),
    path('invoices/<int:invoice_id>/edit/', views.edit_invoice, name='edit_invoice'), # Edit Invoice Header
    
    # 5. DOCUMENT STEP EDITS
    path('dc/<int:invoice_id>/edit/', views.edit_dc, name='edit_dc'),
    path('transport/<int:invoice_id>/edit/', views.edit_transport, name='edit_transport'),
    path('confirmation/<int:invoice_id>/', views.create_confirmation, name='create_confirmation'),
    path('confirmation/<int:invoice_id>/finalize/', views.finalize_invoice_pdf, name='finalize_invoice_pdf'), # NEW

    # 6. CONFIRMATION DETAIL ACTIONS
    path('images/<int:image_id>/delete/', views.delete_packed_image, name='delete_packed_image'),
    
    # 7. PRINT VIEW
    path('invoices/<int:invoice_id>/print/', views.print_invoice, name='print_invoice'),
    path('invoices/<int:invoice_id>/print-dc/', views.print_dc, name='print_dc'),
    
    # 8. DETAIL VIEWS
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('invoices/<int:invoice_id>/print-transport/', views.print_transport, name='print_transport'),

    # 8. TRASH & RESTORE
    path('trash/', views.trash_list, name='trash_list'),
    path('delete/<str:model_name>/<int:pk>/', views.delete_object, name='delete_object'),
    path('restore/<str:model_name>/<int:pk>/', views.restore_object, name='restore_object'),
    path('hard-delete/<str:model_name>/<int:pk>/', views.hard_delete_object, name='hard_delete_object'),
    
    # 9. PROJECT GUIDE
    path('project-guide/', views.project_guide, name='project_guide'),
]
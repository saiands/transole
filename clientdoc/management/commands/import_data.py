import pandas as pd
from django.core.management.base import BaseCommand
from clientdoc.models import Item, ItemCategory, StoreLocation

class Command(BaseCommand):
    help = 'Imports items and locations from Excel files in Imports folder'

    def handle(self, *args, **kwargs):
        self.import_locations()
        self.import_items()

    def import_locations(self):
        try:
            df = pd.read_excel('Imports/client_location.xlsx')
            count = 0
            for _, row in df.iterrows():
                site_name = str(row.get('Site', '')).strip()
                if not site_name or pd.isna(site_name):
                    continue
                
                StoreLocation.objects.update_or_create(
                    name=site_name,
                    defaults={
                        'site_code': row.get('Site Code', ''),
                        'city': row.get('City', ''),
                        'state': row.get('State', 'Karnataka'),
                        'priority': row.get('Priority\n(P1,P2,P3,P4)', ''),
                        'address': f"{row.get('City', '')}, {row.get('State', '')}"
                    }
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} locations.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing locations: {e}'))

    def import_items(self):
        try:
            df = pd.read_excel('Imports/Transcend Digital Solutions Products.xlsx')
            count = 0
            for _, row in df.iterrows():
                particular = str(row.get('PARTICULAR', '')).strip()
                if not particular or pd.isna(particular):
                    continue
                
                category_name = str(row.get('Details', '')).strip()
                category = None
                if category_name and not pd.isna(category_name):
                    category, _ = ItemCategory.objects.get_or_create(name=category_name)
                
                gst_val = row.get('GST %', 0.18)
                if pd.isna(gst_val): gst_val = 0.18
                
                price_val = row.get('Rate', 0.0)
                if pd.isna(price_val): price_val = 0.0

                Item.objects.update_or_create(
                    name=particular,
                    defaults={
                        'category': category,
                        'article_code': row.get('Article', ''),
                        'gst_rate': gst_val,
                        'price': price_val,
                        'description': row.get('Remarks', '') if not pd.isna(row.get('Remarks', '')) else ''
                    }
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} items.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing items: {e}'))

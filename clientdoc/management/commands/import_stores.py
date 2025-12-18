import csv
from io import StringIO
from django.core.management.base import BaseCommand
from django.db import transaction
from clientdoc.models import StoreLocation

class Command(BaseCommand):
    help = 'Imports store data from embedded CSV data'

    def handle(self, *args, **kwargs):
        # --- Content from STORE DATA.xlsx - Sheet1.csv ---
        csv_data = """Site Code,Store Name,Store Addresses
P533,PT-FORUM NEIGHBOHOOD-BENGALURU,"Pantaloons Shop No. Gf 13 To 17A, The Forum Neighbourhood Mall Bengaluru Karnataka - 560066"
P539,PT-NEELADRI ROAD-BENGALURU,"Pantaloons, GF & FF, Sy No.153/1,Doddathogur, Begur HobliElectronic city phase 1, Bengaluru - 560100"
P613,PT-INFANTRY ROAD-BELLARY,"Pantaloons, GKR Building,S No 78,84/05, \nInfantry Main road, Ram Nagar,New trunk Road,\nBehind Vasavi Schl,Mrc Colony,\nBallari, Ballari, Karnataka, 583104"
P688,PT-MANTRI JUNCTION JP NAGAR-BENGALURU,"Pantaloons, No 45/1and 45/2, 45th cross, JP Nagar 2nd phase Bengaluru Pincode - 560069"
P700,PT-KUVENPU NAGAR-MYSURU,"Pantaloons,Sri Guru Raghavendra Towers"" 556/A, New Kantharaj Urs Road, Saraswatipuram, T K Layout, Mysore PIN No. 570023"
P493,PT-ORION UPTOWN MALL-BENGALURU,"Pantaloons, Ugf - 11, 12 & 13, 7, Orion Uptown Mall Old Madras Road, Huskur, Bengaluru"
P488,PT-BHARTIYA CITY CENTRE-BENGALURU,"Pantaloons, Ugf, No 1Ug, 2Ug Thanisandra Main Road, Bengaluru Bengaluru Karnataka - 560064"
P223,PT-BEARYS MALL-SHIVAMOGGA,"Pantaloons Abfrl, Bearys Mall, Sn Market Ameer Ahmed Circle, Shivamogga Karnataka - 577201"
P427,PT-COMMERCIAL STREET-BENGALURU,"Pantaloons Pt,Lgf,Ugf,Mezz & Ff,Municipal Number 15 Commercial Street, Bangalore Bengaluru Karnataka - 560001"
P435,PT-KAMMANAHALLI-BENGALURU,"Pantaloons, Gf & Ff, Snr Square, No 4/1, Kammanahalli Main Road, Bengaluru, Karna Bengaluru Karnataka - 560084"
P463,PT-LULU GLOBAL MALL-BENGALURU,"Pantaloons, Gf, Lulu Global Mall, Lulu Global Mall, Lulu International Shopping Bengaluru Karnataka - 560023"
P682,PT-NEXUS FIZA MALL-MANGALURU,"Pantaloons, Nexus Fiza Mall, Unit No. Anchor 03-A, First Floor, \nMangaladevi Temple Road, Pand...""
P713,PT-MALL OF ASIA-BENGALURU,"Pantaloons, Gf, Mall of Asia, Phoneix mall of Asia,Bytarayanpura,Bengaluru Karnataka - 560092"
"""

        csvfile = StringIO(csv_data)
        reader = csv.reader(csvfile)
        
        # Skip header
        try:
            next(reader) 
        except StopIteration:
            self.stdout.write(self.style.WARNING("CSV data is empty."))
            return
        
        stores_to_create = []
        
        for row in reader:
            if len(row) < 3:
                continue
                
            store_name = row[1].strip()
            # Clean up newlines, quotes, and inconsistent spacing in the address
            store_address = row[2].strip().replace('\n', ', ').replace('""', '"').strip('"') 
            
            # Check if a store with this name already exists
            if not StoreLocation.objects.filter(name=store_name).exists():
                stores_to_create.append(
                    StoreLocation(
                        name=store_name, 
                        address=store_address
                    )
                )

        if stores_to_create:
            with transaction.atomic():
                StoreLocation.objects.bulk_create(stores_to_create)
            self.stdout.write(self.style.SUCCESS(f"Successfully created {len(stores_to_create)} new StoreLocation records."))
        else:
            self.stdout.write(self.style.SUCCESS("No new stores to create. All listed stores already exist."))

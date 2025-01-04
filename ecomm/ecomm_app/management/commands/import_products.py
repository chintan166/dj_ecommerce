import csv
from django.core.management.base import BaseCommand
from ecomm_app.models import Product
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Import products from a CSV file into the database'

    def handle(self, *args, **kwargs):
        # Define the path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'dummy_products.csv')

        # Open the CSV file and read the data
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)

            for row in csvreader:
                name = row['name']
                description = row['description']
                price = row['price']
                image = row['image']  # Assuming image filenames are stored in the CSV
                
                # Create a new Product object for each row in the CSV
                product = Product(
                    name=name,
                    description=description,
                    price=price,
                    image=f'product_images/{image}'  # Assuming images are stored in 'product_images' folder
                )
                product.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {name}'))

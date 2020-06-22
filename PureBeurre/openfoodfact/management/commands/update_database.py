from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Category, Product


class Command(BaseCommand):
    """
    This class contains custom commands
    """
    help = "command wich update the database"

    def handle(self, *args, **options):
        """
        This method is executed when we call the command and this command
        fill the database
        """
        Product.objects.update_products()
        
        

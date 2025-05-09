import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')  # Replace with your project name
django.setup()


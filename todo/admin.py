print("Registering Todo model")  # Add this

from django.contrib import admin
from .models import Todo

admin.site.register(Todo)

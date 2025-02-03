from django.db import models
from autoslug import AutoSlugField

class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    slug = AutoSlugField(populate_from='get_full_name', unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        """Returns a slug-friendly full name."""
        return f"{self.first_name}-{self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

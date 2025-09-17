import uuid
from django.db import models
from django.utils.text import slugify


# This modele class use for category.
class Category(models.Model):
    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name       = models.CharField(max_length=50, unique=True)
    slug                = models.SlugField(max_length=100, unique=True)
    description         = models.TextField(max_length=255, blank=True)
    category_image      = models.ImageField(upload_to='photos/categories', blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only set slug if empty
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name
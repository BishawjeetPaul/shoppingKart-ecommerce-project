from django.db import models


# This modele class use for category.
class Category(models.Model):
    id                  = models.AutoField(primary_key=True)
    category_name       = models.CharField(max_length=50, unique=True)
    slug                = models.CharField(max_length=100, unique=True)
    descritption        = models.TextField(max_length=255, blank=True)
    cat_image           = models.ImageField(upload_to='photos/categories', blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
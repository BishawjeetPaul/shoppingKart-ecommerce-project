import uuid
from django.db import models
# from category.models import Category
from django.utils.text import slugify
from django.utils.timezone import now


# this function is used to generate category id followed character CAT-6 digit random number
def generate_category_id():
    # Current year + month (e.g. 202509)
    year_month = now().strftime("%Y%m")
    
    # Find last category for this year-month
    last_cat = Category.objects.filter(category_id__startswith=f"CAT{year_month}").order_by('-created_at').first()
    
    if last_cat and last_cat.category_id:
        last_num = int(last_cat.category_id[-4:])  # get last 4 digits
        new_num = last_num + 1
    else:
        new_num = 1

    # Format: CATYYYYMM0001
    return f"CAT{year_month}{new_num:04d}"


class Category(models.Model):
    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_id         = models.CharField(max_length=20, unique=True, editable=False, default=generate_category_id)
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
        return f"{self.category_id} - self.name"
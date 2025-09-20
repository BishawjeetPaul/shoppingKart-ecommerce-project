import uuid
from django.utils.text import slugify
from django.utils.timezone import now
from django.db import models
from category.models import Category
from django.urls import reverse



# this function is used to generate product id followed character KART-6 digit random number
def generate_product_id():
    # Current year + month (e.g. 202509)
    year_month = now().strftime("%Y%m")
    
    # Find last category for this year-month
    last_pro = Product.objects.filter(product_id__startswith=f"KART{year_month}").order_by('-created_at').first()
    
    if last_pro and last_pro.product_id:
        last_num = int(last_pro.product_id[-6:])  # get last 4 digits
        new_num = last_num + 1
    else:
        new_num = 1

    # Format: KARTYYYYMM0001
    return f"KART{year_month}{new_num:06d}"


class Product(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id              = models.CharField(max_length=20, unique=True, editable=False, default=generate_product_id)
    product_name            = models.CharField(max_length=200, unique=True)
    slug                    = models.SlugField(max_length=100, unique=True)
    product_description     = models.TextField(max_length=500, blank=True)
    product_price           = models.IntegerField()
    product_image           = models.ImageField(upload_to='photos/products')
    stock                   = models.IntegerField()
    is_available            = models.BooleanField(default=True)
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)
    isDelete                = models.BooleanField(default=False)
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only set slug if empty
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('product-details', args=[self.category.slug, self.slug])

    def __str__(self):
        return f"{self.product_id}- {self.product_name}"

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver



# This model table is used for CustomUsers.
class CustomUser(AbstractUser):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type_data  = ((1,"ADMIN"), (2,"Customers"))
    user_type       = models.CharField(default=1, choices=user_type_data, max_length=10)


# This model table is used for Main-User.
class AdminUser(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin           = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender          = models.CharField(max_length=10)
    phone_number    = models.CharField(max_length=50)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now_add=True)
    objects         = models.Manager()


# This model table is used for Customers.
class Customer(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin           = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender          = models.CharField(max_length=10)
    phone_number    = models.CharField(max_length=50)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now_add=True)
    objects         = models.Manager()


# This model table is used for Customer-Address.
class CustomerAddress(models.Model):
    """
    Stores multiple address for each customer (User).
    Useful for shipping, billing, etc.
    """
    ADDRESS_TYPES   = (
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other')
    )

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin           = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    customer_id     = models.ForeignKey(Customer, on_delete=models.CASCADE)
    full_name       = models.CharField(max_length=50)
    phone_number    = models.CharField(max_length=50)
    alt_ph_number   = models.CharField(max_length=50)
    pincode         = models.CharField(max_length=10)
    house_no        = models.CharField(max_length=10)
    street          = models.CharField(max_length=255, blank=True, null=True)
    landmark        = models.CharField(max_length=255, blank=True, null=True)
    city            = models.CharField(max_length=50)
    state           = models.CharField(max_length=50)
    Cuntry          = models.CharField(max_length=50, default="India")

    address_type    = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home')
    is_default      = models.BooleanField(default=False)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now_add=True)
    objects         = models.Manager()

    class Meta:
        verbose_name_plural = "Customer Addresses"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name, {self.city} ({self.address_type})}"
    

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminUser.objects.create(admin=instance)
        if instance.user_type==2:
            Customer.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type==1:
        instance.adminuser.save()
    if instance.user_type==2:
        instance.customer.save()



# class Account(AbstractBaseUser):
#     last_name       = models.CharField(max_length=50)
#     username        = models.CharField(max_length=50, unique=True)
#     email           = models.EmailField(max_length=100, unique=True)
#     phone_number    = models.CharField(max_length=50)

#     # required
#     date_joined     = models.DateTimeField(auto_now_add=True)
#     last_login      = models.DateTimeField(auto_now_add=True)
#     is_admin        = models.BooleanField(default=False)
#     is_staff        = models.BooleanField(default=False)
#     is_active        = models.BooleanField(default=False)
#     is_superadmin        = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

#     objects = MyAccountManager()

#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_admin

#     def has_module_perms(self, add_label):
#         return True

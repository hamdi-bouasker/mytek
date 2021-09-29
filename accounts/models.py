from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, f_name, l_name, email, password=None):
        if not email:
            raise ValueError('Please provide valid email address.')

        user = self.model(
            email = self.normalize_email(email),
            f_name = f_name,
            l_name = l_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, f_name, l_name, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            f_name = f_name,
            l_name = l_name,
            password = password
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)

        return user

class Account(AbstractBaseUser):
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    tel = models.CharField(max_length=50, unique=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['f_name', 'l_name']

    objects = MyAccountManager()

    def fullname(self):
        return f"{self.f_name} {self.l_name}"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.f_name

    def fulllocation(self):
        return f"{self.city}, {self.state}, {self.country}"


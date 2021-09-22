from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, f_name, l_name, email, password=None):
        if not email:
            raise ValueError('Please provide valid email address.')

        # if not username:
        #     raise ValueError('Please provide valid username.')

        user = self.model(
            email = self.normalize_email(email),
            f_name = f_name,
            l_name = l_name
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

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['f_name', 'l_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


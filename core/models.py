
from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    )
from django.conf import settings

class UserManager(BaseUserManager):
    
    def create_user(self, email, password, **extras):
        if len(email.strip()) < 1:
            raise ValueError('Email Cannot be Empty')
        user = self.model(email=self.normalize_email(email), **extras)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extras):

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin ):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, null=True)
    is_staff = models.BooleanField(default=False, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Recipe(models.Model):
    '''
        Recipe Object
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE #IF USER IS DELETED ALL THE RELATED DATA WILL BE REMOVED!
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

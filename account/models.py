from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('candidate', 'Candidate'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='admin')
    email = models.EmailField(unique=True, validators=[EmailValidator(message='Enter a valid email address.')])
    is_verified = models.BooleanField(default=False)
    created_by_admin = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='created_users')
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    


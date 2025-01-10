from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)  # Hash the password

        try:
            user.full_clean()  # This triggers validation, including email validation
        except ValidationError as e:
            raise ValidationError(f"Validation failed: {e}")

        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='UserID')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)  # User is inactive until email is confirmed
    is_staff = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)  # New field for email confirmation

    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

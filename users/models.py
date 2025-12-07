from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """
    Model representing user roles in the system.
    """
    ROLE_CHOICES = [
        ('operador', 'Operador'),
        ('chefe', 'Chefe'),
        ('admin', 'Admin'),
        ('superadmin', 'Super Admin'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    """
    Custom user model with role-based permissions.
    """
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField(Role, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def has_role(self, role_name):
        """Check if user has a specific role."""
        return self.roles.filter(name=role_name).exists()
    
    def is_operador(self):
        return self.has_role('operador')
    
    def is_chefe(self):
        return self.has_role('chefe')
    
    def is_admin(self):
        return self.has_role('admin')
    
    def is_superadmin(self):
        return self.has_role('superadmin')
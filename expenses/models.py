from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import TransactionQuerySet
class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Avoid clash with default User model
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Avoid clash with default User model
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')  # Link to User
    date = models.DateField() 
    category = models.ForeignKey(Category,on_delete=models.CASCADE)  # Example: "Groceries", "Rent"
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)  # 'income' or 'expense'
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Example: 100.50
    description = models.TextField(blank=True, null=True)  # Optional transaction details

    objects= TransactionQuerySet.as_manager()
    
    def __str__(self):
        return f"{self.date} - {self.category} - {self.type} - {self.amount}"
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')  # Associate feedback with user
    bio = models.TextField()  # Feedback message
    submitted_at = models.DateTimeField(auto_now_add=True)  # Automatically record submission time

    def __str__(self):
        return f"Feedback from {self.user.username} at {self.submitted_at}"
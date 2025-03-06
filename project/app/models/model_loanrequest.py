from django.db import models
from app.models.users import UserProfile
from django.utils import timezone
class LoanRequest(models.Model):
    """
    Model for loan requests.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    advisor = models.ForeignKey(UserProfile, related_name='advisor_loan_requests', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)  # Last update
    
    # Loan attributes
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Loan amount
    term = models.IntegerField()  # Loan term in months
    
    # Loan request attributes
    low_doc = models.CharField(max_length=1, choices=[('1', 'Yes'), ('0', 'No')])  # LowDoc = 1 or 0
    rev_line_cr = models.CharField(max_length=1, choices=[('1', 'Yes'), ('0', 'No')])  # RevLineCr = 1 or 0
    no_emp = models.FloatField()  # Number of employees
    naics = models.CharField(max_length=2)  # NAICS code
    new = models.CharField(max_length=1, choices=[('1', 'New'), ('0', 'Existing')])  # New = 1 or 0
    franchise = models.CharField(max_length=1, choices=[('1', 'Franchise'), ('0', 'Non-Franchise')])  # Franchise = 1 or 0

    # Location attributes
    state = models.CharField(max_length=2)  # State abbreviation
    rural = models.CharField(max_length=4, choices=[('0', 'Urban'), ('1', 'Rural'), ('None', 'Undefined')])  # Urban, Rural or Undefined
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"LoanRequest #{self.id} - {self.status} - {self.amount}€ ({self.user.username})"
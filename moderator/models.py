from django.db import models
from accounts.models import User
# Create your models here.
class Material(models.Model):
    name = models.CharField(max_length=50)
    total_quantity = models.PositiveIntegerField(default=0)
    available_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class LoanApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    is_pending = models.BooleanField(default=True) 
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} | {self.material} | {self.is_pending} | {self.is_approved}'
    
    class Meta:
        ordering = ['-created_at']
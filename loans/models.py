from django.db import models
from accounts.models import User
from moderator.models import Material


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user')
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    who_approved = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='who_approved', null=True, blank=True)
    quantity = models.PositiveIntegerField()
    expected_return_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)
    is_return_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} | {self.material} | {self.is_returned} | {self.is_return_confirmed}'
    
    class Meta:
        ordering = ['-created_at']

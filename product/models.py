from django.db import models
from user.models import User
import uuid
 


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



    class Meta:
        ordering = ('-created', '-updated',)

    def __str__(self):
        return self.name









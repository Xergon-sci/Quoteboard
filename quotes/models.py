from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import secrets

class Board(models.Model):
    code = models.CharField(max_length=8, unique=True, editable=False, blank=True, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    date = models.DateField(auto_now_add=True, null=False)
    pin = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)], blank=True, null=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = secrets.token_urlsafe(6)[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='quotes', on_delete=models.CASCADE)

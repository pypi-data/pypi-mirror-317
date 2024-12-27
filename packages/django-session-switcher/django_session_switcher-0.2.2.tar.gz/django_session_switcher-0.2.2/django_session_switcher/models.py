from django.db import models


# Create your models here.
class SessionUser(models.Model):
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Switchable User"
        verbose_name_plural = "Switchable Users"
        ordering = ['username']

    def __str__(self):
        return self.username

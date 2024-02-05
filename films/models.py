from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

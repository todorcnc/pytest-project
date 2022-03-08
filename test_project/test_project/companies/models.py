from django.db import models
from django.db.models import URLField
from django.utils.timezone import now

# Create your models here.


class Company(models.Model):
    class CompanyStatus(models.TextChoices):
        LAYOFFS = "Layoffs"
        HIRING_FREEZE = "Hiring Freeze"
        HIRING = "Hiring"

    name = models.CharField(max_length=200, unique=True)
    status = models.CharField(
        choices=CompanyStatus.choices, default=CompanyStatus.HIRING, max_length=100
    )
    last_update = models.DateTimeField(default=now, editable=True)
    application_link = URLField(blank=True)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self) -> str:
        return self.name

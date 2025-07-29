from django.db import models
from django.utils import timezone

class Nourriture(models.Model):
    IdEtablissement = models.ForeignKey(
        'etablissements.Etablissement',
        on_delete=models.CASCADE,
        related_name='nourritures'
    )
    Nom = models.CharField(max_length=100)
    Prix = models.DecimalField(max_digits=10, decimal_places=2)
    Photo = models.ImageField(upload_to='foods/photos/', blank=True, null=True)
    Temps_preparation = models.PositiveIntegerField(help_text="Temps en minutes")
    Description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modify_at = models.DateTimeField(auto_now=True)

    
    
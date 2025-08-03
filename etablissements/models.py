from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Etablissement(models.Model):
    IdUser = models.ForeignKey(
        'utilisateurs.User',
        on_delete=models.CASCADE,
        related_name='etablissements'
    )
    Nom = models.CharField(max_length=100)
    Photo_de_couverture = models.ImageField(upload_to='etablissements/couvertures/', blank=True, null=True)
    Description = models.TextField(blank=True)
    Horaire_ouverture = models.CharField(max_length=1000, blank=True)
    Emplacement = models.CharField(max_length=255)  
    Active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    modify_at = models.DateTimeField(auto_now=True)

class HoraireOuverture(models.Model):
    JOURS_SEMAINE = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]

    etablissement = models.ForeignKey(
        'Etablissement',
        on_delete=models.CASCADE,
        related_name='horaires'
    )
    jour = models.PositiveSmallIntegerField(choices=JOURS_SEMAINE)
    ouverture_matin = models.TimeField(null=True, blank=True)
    fermeture_matin = models.TimeField(null=True, blank=True)
    ouverture_soir = models.TimeField(null=True, blank=True)
    fermeture_soir = models.TimeField(null=True, blank=True)
    est_ferme = models.BooleanField(default=False)

    class Meta:
        unique_together = ('etablissement', 'jour')
        ordering = ['jour']

    def __str__(self):
        if self.est_ferme:
            return f"{self.get_jour_display()} : Fermé"
        
        horaires = []
        if self.ouverture_matin:
            horaires.append(f"Matin: {self.ouverture_matin.strftime('%H:%M')}-{self.fermeture_matin.strftime('%H:%M')}")
        if self.ouverture_soir:
            horaires.append(f"Soir: {self.ouverture_soir.strftime('%H:%M')}-{self.fermeture_soir.strftime('%H:%M')}")
        
        return f"{self.get_jour_display()} : {' | '.join(horaires) if horaires else 'Ouvert 24h/24'}"


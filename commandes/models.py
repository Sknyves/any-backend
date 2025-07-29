from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from etablissements.models import HoraireOuverture

class Commande(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('preparation', 'En préparation'),
        ('livraison', 'En livraison'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    IdFood = models.ForeignKey(
        'nourritures.Nourriture',
        on_delete=models.SET_NULL,
        null=True,
        related_name='commandes'
    )
    Adresse_livraison = models.TextField()
    Date_heure_livraison = models.DateTimeField()
    IdUser = models.ForeignKey(
        'utilisateurs.User',
        on_delete=models.CASCADE,
        related_name='commandes'
    )
    Statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='en_attente'
    )
    created_at = models.DateTimeField(default=timezone.now)
    modify_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        
        # Vérification des horaires d'ouverture
        if not self.est_dans_les_horaires_ouverture():
            raise ValidationError("L'établissement est fermé à cette heure")

    def est_dans_les_horaires_ouverture(self):
        jour_semaine = self.Date_heure_livraison.weekday()
        heure_livraison = self.Date_heure_livraison.time()
        
        try:
            horaire = self.IdFood.IdEtablissement.horaires.get(jour=jour_semaine)
        except HoraireOuverture.DoesNotExist:
            return False
        
        if horaire.est_ferme:
            return False
        
        # Vérification plage horaire matin
        if (horaire.ouverture_matin and 
            horaire.fermeture_matin and
            horaire.ouverture_matin <= heure_livraison <= horaire.fermeture_matin):
            return True
        
        # Vérification plage horaire soir
        if (horaire.ouverture_soir and 
            horaire.fermeture_soir and
            horaire.ouverture_soir <= heure_livraison <= horaire.fermeture_soir):
            return True
        
        return False


from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Nourriture(models.Model):
    IdEtablissement = models.ForeignKey(
        'etablissements.Etablissement',
        on_delete=models.CASCADE,
        related_name='nourritures'
    )
    Nom = models.CharField(max_length=100)
    Prix = models.DecimalField(max_digits=10, decimal_places=2)
    Photo = models.ImageField(upload_to='foods/photos/', blank=True, null=True)
    Temps_preparation = models.PositiveIntegerField(
        help_text="Temps en minutes",
        validators=[MinValueValidator(1)]
    )
    Description = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)
    Note = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    nb_avis = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    modify_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Nourriture"
        verbose_name_plural = "Nourritures"
        ordering = ['-disponible', 'Nom']

    def __str__(self):
        return f"{self.Nom} ({self.IdEtablissement.Nom})"

    def update_rating(self, new_rating):
        """
        Met à jour la note moyenne de manière atomique
        Évite les problèmes de concurrence
        """
        from django.db.models import F
        
        # Validation de la note
        if not (1 <= new_rating <= 5):
            raise ValueError("La note doit être entre 1 et 5")

        # Calcul atomique pour éviter les race conditions
        Nourriture.objects.filter(pk=self.pk).update(
            Note=(
                (F('Note') * F('nb_avis') + new_rating) / 
                (F('nb_avis') + 1)
            ),
            nb_avis=F('nb_avis') + 1
        )

        # Rafraîchir l'instance depuis la base de données
        self.refresh_from_db()

    def get_rating_display(self):
        """
        Retourne la note formatée avec le nombre d'avis
        """
        if self.nb_avis == 0:
            return "Pas encore noté"
        return f"{float(self.Note):.1f}/5 ({self.nb_avis} avis)"

    def clean(self):
        """
        Validation supplémentaire avant sauvegarde
        """
        if self.Prix < 0:
            raise ValidationError({"Prix": "Le prix ne peut pas être négatif"})
        
        if self.Temps_preparation < 1:
            raise ValidationError({"Temps_preparation": "Le temps doit être d'au moins 1 minute"})
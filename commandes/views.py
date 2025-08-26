from rest_framework import viewsets
from commandes.models import Commande
from commandes.serializers import CommandeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, F, Q, Prefetch
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from etablissements.models import Etablissement
from nourritures.models import Nourriture
from utilisateurs.models import User

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['IdUser', 'Statut']
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(IdUser=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats_etablissement(request, etablissement_id):
    try:
        etablissement = Etablissement.objects.get(id=etablissement_id)
        
        # Vérifier que l'utilisateur est bien le propriétaire
        if etablissement.IdUser != request.user:
            return Response({"error": "Accès non autorisé"}, status=403)
        
        # Période : 30 derniers jours
        date_debut = timezone.now() - timedelta(days=30)
        
        # Commandes de l'établissement
        commandes_etablissement = Commande.objects.filter(
            IdFood__IdEtablissement=etablissement,
            created_at__gte=date_debut
        )
        
        # Chiffre d'affaires (somme des prix des nourritures commandées)
        chiffre_affaires = commandes_etablissement.aggregate(
            total=Sum('IdFood__Prix')
        )['total'] or 0
        
        # Nombre total de commandes
        total_commandes = commandes_etablissement.count()
        
        # Commandes par jour (7 derniers jours)
        commandes_par_jour = {}
        jours_fr = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        
        for i in range(7):
            date = timezone.now() - timedelta(days=i)
            count = Commande.objects.filter(
                IdFood__IdEtablissement=etablissement,
                created_at__date=date.date()
            ).count()
            commandes_par_jour[jours_fr[date.weekday()]] = count
        
        # Plats les plus vendus
        plats_vendus = Commande.objects.filter(
            IdFood__IdEtablissement=etablissement,
            created_at__gte=date_debut
        ).values('IdFood__Nom').annotate(
            total_vendu=Count('id')
        ).order_by('-total_vendu')[:5]
        
        plats_vendus_dict = {item['IdFood__Nom']: item['total_vendu'] for item in plats_vendus}
        
        # Note moyenne des plats de l'établissement
        note_moyenne = Nourriture.objects.filter(
            IdEtablissement=etablissement
        ).aggregate(moyenne=Avg('Note'))['moyenne'] or 0
        
        # Plat le plus populaire (meilleure note avec au moins 5 avis)
        plat_populaire = Nourriture.objects.filter(
            IdEtablissement=etablissement,
            nb_avis__gte=5
        ).order_by('-Note').first()
        
        # Statistiques de statut des commandes
        statuts_commandes = commandes_etablissement.values('Statut').annotate(
            count=Count('id')
        )
        
        data = {
            'chiffre_affaires': float(chiffre_affaires),
            'total_commandes': total_commandes,
            'note_moyenne': round(float(note_moyenne), 1),
            'plat_populaire': plat_populaire.Nom if plat_populaire else "Aucun",
            'commandes_par_jour': commandes_par_jour,
            'plats_vendus': plats_vendus_dict,
            'statuts_commandes': {item['Statut']: item['count'] for item in statuts_commandes}
        }
        
        return Response(data)
        
    except Etablissement.DoesNotExist:
        return Response({"error": "Établissement non trouvé"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def commandes_etablissements_utilisateur(request):
    print("🟢 Vue commandes_etablissements_utilisateur appelée!")
    print(f"👤 Utilisateur: {request.user}")
    print(f"📋 Méthode: {request.method}")
    print(f"🔗 URL complète: {request.build_absolute_uri()}")
    print(f"🎯 Chemin: {request.path}")
    print(f"🔍 Query params: {dict(request.GET)}")
    try:
        # Récupérer les établissements de l'utilisateur
        etablissements_utilisateur = Etablissement.objects.filter(IdUser=request.user)
        
        # Filtres
        statut = request.GET.get('statut')
        etablissement_id = request.GET.get('etablissement')
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')
        
        # Commandes des établissements de l'utilisateur
        commandes = Commande.objects.filter(
            IdFood__IdEtablissement__in=etablissements_utilisateur
        ).select_related(
            'IdFood', 
            'IdFood__IdEtablissement', 
            'IdUser'
        ).order_by('-created_at')
        
        # Appliquer les filtres
        if statut:
            commandes = commandes.filter(Statut=statut)
        if etablissement_id:
            commandes = commandes.filter(IdFood__IdEtablissement_id=etablissement_id)
        if date_debut:
            commandes = commandes.filter(created_at__date__gte=date_debut)
        if date_fin:
            commandes = commandes.filter(created_at__date__lte=date_fin)
        
        # Pagination
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 20)
        paginator = Paginator(commandes, per_page)
        
        page_obj = paginator.get_page(page)
        
        # Statistiques
        stats = {
            'total_commandes': commandes.count(),
            'commandes_par_statut': commandes.values('Statut').annotate(count=Count('id')),
            'chiffre_affaires': commandes.filter(Statut='livree').aggregate(
                total=Sum('IdFood__Prix')
            )['total'] or 0,
            'commandes_aujourdhui': commandes.filter(
                created_at__date=timezone.now().date()
            ).count()
        }
        
        data = {
            'commandes': [
                {
                    'id': commande.id,
                    'plat_nom': commande.IdFood.Nom,
                    'plat_prix': float(commande.IdFood.Prix),
                    'etablissement_nom': commande.IdFood.IdEtablissement.Nom,
                    'etablissement_id': commande.IdFood.IdEtablissement.id,
                    'client_nom': f"{commande.IdUser.first_name} {commande.IdUser.last_name}",
                    'client_email': commande.IdUser.email,
                    'adresse_livraison': commande.Adresse_livraison,
                    'date_heure_livraison': commande.Date_heure_livraison,
                    'statut': commande.Statut,
                    'date_creation': commande.created_at,
                    'date_modification': commande.modify_at
                }
                for commande in page_obj
            ],
            'pagination': {
                'page': page_obj.number,
                'pages': paginator.num_pages,
                'total': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            },
            'statistiques': stats,
            'filtres': {
                'statuts': dict(Commande.STATUS_CHOICES),
                'etablissements': [
                    {'id': etab.id, 'nom': etab.Nom}
                    for etab in etablissements_utilisateur
                ]
            }
        }
        
        return Response(data)
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)
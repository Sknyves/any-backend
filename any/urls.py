from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/utilisateurs/', include('utilisateurs.urls')),
    path('api/etablissements/', include('etablissements.urls')),
    path('api/nourritures/', include('nourritures.urls')),
    path('api/commandes/', include('commandes.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
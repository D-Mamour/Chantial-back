"""Vues d'inscription, connexion et profil."""
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import InscriptionSerializer, ConnexionSerializer, UtilisateurSerializer

class InscriptionView(generics.CreateAPIView):
    """Crée un compte Chantial."""
    serializer_class = InscriptionSerializer
    permission_classes = [permissions.AllowAny]

class ConnexionView(APIView):
    """Retourne des jetons JWT après authentification."""
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        """Traite la connexion."""
        s = ConnexionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        u = s.validated_data["utilisateur"]
        refresh = RefreshToken.for_user(u)
        return Response({"access":str(refresh.access_token),"refresh":str(refresh),
                         "utilisateur":UtilisateurSerializer(u).data})

class ProfilView(generics.RetrieveUpdateAPIView):
    """Consulte ou modifie le profil connecté."""
    serializer_class = UtilisateurSerializer
    def get_object(self):
        """Retourne le compte authentifié."""
        return self.request.user

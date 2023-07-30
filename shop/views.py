from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product, Favorite
from .permission import IsAuthor
from .serializers import CreateProductSerializer, ProductListSerializer, ProductDetailSerializer, FavoriteProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        return CreateProductSerializer

    @action(['POST'], detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        product = self.get_object()
        user = request.user
        try:
            favorite = Favorite.objects.get(product=product, user=user)
            favorite.is_favorite = not favorite.is_favorite
            if favorite.is_favorite:
                favorite.save()
            else:
                favorite.delete()
            message = 'добавлено в избранных' if favorite.is_favorite else 'удалено из избранных'
        except Favorite.DoesNotExist:
            Favorite.objects.create(product=product, user=user, is_favorite=True)
            message = 'добавленно в избранных'
        return Response(message, status=200)
    

class FavoritesListView(ListAPIView):
    permission_classes = [IsAuthor] #чтобы только сам мог удалить или добавить в избранное
    serializer_class = FavoriteProductSerializer

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)

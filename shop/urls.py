from django.urls import path, include
from rest_framework.routers import SimpleRouter


from .views import ProductViewSet, FavoritesListView

router = SimpleRouter()
router.register('products', ProductViewSet, 'products')


urlpatterns = [
    path('', include(router.urls)),
    path('favorites_list/', FavoritesListView.as_view()),
]

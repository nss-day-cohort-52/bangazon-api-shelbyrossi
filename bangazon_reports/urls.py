from django.urls import path
from .views import ProductPriceList
from .views import FavoriteStores

urlpatterns = [
    path('reports/products', ProductPriceList.as_view()),
    path('reports/stores', FavoriteStores.as_view())
]

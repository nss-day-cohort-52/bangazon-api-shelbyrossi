from django.urls import path
from .views import ProductPriceList
from .views import FavoriteStores
from .views import InexpensiveProducts

urlpatterns = [
    path('reports/products', ProductPriceList.as_view()),
    path('reports/stores', FavoriteStores.as_view()),
    path('reports/inexpensiveproducts', InexpensiveProducts.as_view()),
]

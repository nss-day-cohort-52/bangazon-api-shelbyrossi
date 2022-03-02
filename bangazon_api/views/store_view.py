from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db.models import Q, Count
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from bangazon_api.models import Store
from bangazon_api.serializers import StoreSerializer, MessageSerializer, AddStoreSerializer
from bangazon_api.models import Favorite

class StoreView(ViewSet):
    @swagger_auto_schema(
        request_body=AddStoreSerializer(),
        responses={
            201: openapi.Response(
                description="The requested product",
                schema=StoreSerializer()
            ),
            400: openapi.Response(
                description="Validation Error",
                schema=MessageSerializer()
            ),
        }
    )
    def create(self, request):
        """Create a store for the current user"""
        try:
            store = Store.objects.create(
                seller=request.auth.user,
                name=request.data['name'],
                description=request.data['description']
            )
            serializer = StoreSerializer(store)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of all stores",
                schema=StoreSerializer(many=True)
            )
        }
    )
    def list(self, request):
        """Get a list of all stores"""
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="The requested store",
                schema=StoreSerializer()
            ),
            404: openapi.Response(
                description="The requested store does not exist",
                schema=MessageSerializer()
            ),
        }
    )
    def retrieve(self, request, pk):
        """Get a single store"""
        try:
            store = Store.objects.annotate(is_favorite=Count(
                'favorites',
                filter=Q(favorites=request.auth.user)
            )).get(pk=pk)
            serializer = StoreSerializer(store)
            return Response(serializer.data)
        except Store.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=AddStoreSerializer(),
        responses={
            204: openapi.Response(
                description="No content, store successfully updated",
                schema=StoreSerializer()
            ),
            400: openapi.Response(
                description="Validation Error",
                schema=MessageSerializer()
            ),
            404: openapi.Response(
                description="Store not found",
                schema=MessageSerializer()
            ),
        }
    )
    def update(self, request, pk):
        """Update a store"""
        try:
            store = Store.objects.get(pk=pk)
            store.name = request.data['name']
            store.description = request.data['description']
            store.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Store.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        
    @action(methods=['post'], detail=True)
    def favorite(self, request, pk):
        """Adding Favorites to a current user"""
        
        try:
    
            store = Store.objects.get(pk=pk)
            user = request.auth.user
            favorite = Favorite()
            favorite.store_id = store.id
            favorite.customer_id = user.id
            favorite.save()
            return Response({'message': 'favorite added!'}, status=status.HTTP_201_CREATED)
        except Store.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    @action(methods=['delete'], detail=True)
    def unfavorite(self, request, pk):
        """delete favorite store
        """
        try:
            favorite = Favorite.objects.get(store_id=pk, customer_id=request.auth.user.id)
            favorite.delete()
            return Response({'message': "You removed this store as a favorite."}, status=status.HTTP_201_CREATED)
        except (Store.DoesNotExist) as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        
        
  
            
        
        
 
        
    
   
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import InformacaoSuspeita
from .serializers import InformacaoSuspeitaSerializer
from facial_recognition.models import Suspect
import json


class InformacaoSuspeitaListCreateView(generics.ListCreateAPIView):
    serializer_class = InformacaoSuspeitaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = InformacaoSuspeita.objects.all()
        
        # Filter by suspect ID if provided
        suspect_id = self.request.query_params.get('suspect', None)
        if suspect_id is not None:
            queryset = queryset.filter(suspect_id=suspect_id)
            
        return queryset

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if suspect_id is provided and exists
        suspect_id = request.data.get('suspect')
        if suspect_id:
            try:
                suspect = Suspect.objects.get(id=suspect_id)
                serializer.save(criado_por=self.request.user, suspect=suspect)
            except Suspect.DoesNotExist:
                return Response(
                    {'error': 'Suspect not found'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            serializer.save(criado_por=self.request.user)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InformacaoSuspeitaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InformacaoSuspeita.objects.all()
    serializer_class = InformacaoSuspeitaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Check if suspect_id is provided and exists
        suspect_id = request.data.get('suspect')
        if suspect_id:
            try:
                suspect = Suspect.objects.get(id=suspect_id)
                serializer.save(suspect=suspect)
            except Suspect.DoesNotExist:
                return Response(
                    {'error': 'Suspect not found'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            serializer.save()
        
        return Response(serializer.data)
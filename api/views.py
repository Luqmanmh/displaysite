from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import patdataSerializer
from displaysite.models import *
from rest_framework.parsers import MultiPartParser, FormParser


class DataUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = patdataSerializer

    def post(self, request):        
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

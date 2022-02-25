from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets
from validaciones.models import *
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class ValidationViewSet(viewsets.ModelViewSet):

	queryset = Validation.objects.all()
	serializer_class = ValidationSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['type', 'risk']


class CostViewSet(viewsets.ModelViewSet):
	queryset = Cost.objects.all()
	serializer_class = CostSerializer

class ProfitabilityViewSet(viewsets.ModelViewSet):
	queryset = Profitability.objects.all()
	serializer_class = ProfitabilitySerializer

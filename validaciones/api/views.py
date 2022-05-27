from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets
from validaciones.models import *
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics

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

class updateValidation(generics.ListCreateAPIView):
	
	queryset = Validation.objects.all()
	serializer_class = ValidationSerializer

	def post(self, request):
		id  = request.data.get('id')
		costs  = request.data.get('costs')
		uuid  = request.data.get('uuid')
		calculation_type  = request.data.get('calculation_type')
		reference  = request.data.get('reference')
		make  = request.data.get('make')
		model  = request.data.get('model')
		amount_purchase  = request.data.get('amount_purchase')
		purchase_vat  = request.data.get('purchase_vat')
		amount_sale  = request.data.get('amount_sale')
		sale_vat  = request.data.get('sale_vat')
		margin  = request.data.get('margin')
		risk  = request.data.get('risk')
		type  = request.data.get('type')

		validation_obj = Validation.objects.get(id=id)
		newcostId = []
		for c in costs:
			newcostId.append(c['cost'])
			for c2 in validation_obj.costs.all():
				if c2.cost.id == c['cost']:
					c2.quantity = c['quantity']
					c2.amount = c['amount']
					c2.save()
		
		costId = []
		for c in validation_obj.costs.all():
			costId.append(c.cost.id)

		for c in costs:
			if c['cost'] not in costId:
				costObj = Cost.objects.get(id=c['cost'])
				costQuantity_ob = CostQuantity.objects.create(uuid=c['uuid'],cost=costObj, quantity=c['quantity'],amount=c['amount'])
				costQuantity_ob.save()
				validation_obj.costs.add(costQuantity_ob)

		for c2 in validation_obj.costs.all():
			if c2.cost.id not in newcostId:
				validation_obj.costs.remove(c2)

		validation_obj.calculation_type = calculation_type
		validation_obj.reference = reference
		validation_obj.make = make
		validation_obj.model = model
		validation_obj.amount_purchase = amount_purchase
		validation_obj.amount_sale = amount_sale
		validation_obj.sale_vat = sale_vat
		validation_obj.purchase_vat = purchase_vat
		validation_obj.margin = margin
		validation_obj.risk = risk
		validation_obj.type = type
		validation_obj.save()
		return Response({"state":0})

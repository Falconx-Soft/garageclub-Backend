from rest_framework import serializers
from validaciones.models import CostQuantity, Validation, Cost, Vat, Profitability
from rest_framework.response import Response


class VATSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vat
        exclude = ['created_at', 'deleted_at', 'updated_at']


class CostSerializer(serializers.ModelSerializer):
    vat = VATSerializer()

    class Meta:
        model = Cost
        exclude = ['created_at', 'deleted_at', 'updated_at']

class CostQuantitySerializer(serializers.ModelSerializer):

    class Meta:
        model = CostQuantity
        exclude = ['created_at', 'deleted_at', 'updated_at']

class ProfitabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Profitability
        fields = '__all__'

class ValidationSerializer(serializers.ModelSerializer):
    costs = CostQuantitySerializer(many=True)

    class Meta:
        model = Validation
        exclude = ['deleted_at', 'updated_at']
        depth = 1

    def create(self, validated_data):
        costs = validated_data.pop('costs')
        print(costs)

        costs = map(lambda cost: {**cost, "amount": cost['cost'].amount * cost['quantity']}, costs)
        costs = list(map(lambda cost: CostQuantity.objects.create(**cost), costs))

        validation = Validation.objects.create(**validated_data)
        print(costs)

        validation.costs.add(*costs)
        costs_sum = sum(cost.amount for cost in costs)
        print(costs_sum)
        validation.save()
        return validation

    def update(self, request, *args, **kwargs):
        validation_obj = Validation.objects.get()

        data = request.data
        
        for c in data.costs:
            print(c,"HEre we are")

        costs_obj = CostQuantity.objects.filter(costs = data.costs)
        validation_obj.reference = "updated"

        validation_obj.save()

        return Response({"success":1})
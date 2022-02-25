from rest_framework import serializers
from validaciones.models import CostQuantity, Validation, Cost, Vat, Profitability


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
    #     depth = 1

    # def create(self, validated_data):
    #     costs = validated_data.pop('costs')
    #     print(costs)

    #     costs = map(lambda cost: {**cost, "amount": cost['cost'].amount * cost['quantity']}, costs)
    #     costs = list(map(lambda cost: CostQuantity.objects.create(**cost), costs))

    #     validation = Validation.objects.create(**validated_data)
    #     print(costs)

    #     validation.costs.add(*costs)
    #     costs_sum = sum(cost.amount for cost in costs)
    #     print(costs_sum)

    #     if validation.calculation_type == 1:
    #         net_margin = validation.amount_purchase - validation.amount_sale
    #         net_margin = net_margin - costs_sum
    #         print(net_margin)

    #     elif validation.calculation_type == 0:
            
    #         validation.sale_vat = True
            
    #         gross_margin = validation.amount_sale - validation.amount_purchase
    #         net_margin = gross_margin / (1 + 0.21) 

    #         net_margin = net_margin - costs_sum
    #         print(net_margin)

    #     validation.margin = float('{:.2f}'.format(net_margin))
    #     validation.save()


    #     return validation
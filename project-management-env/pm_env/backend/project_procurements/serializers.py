from rest_framework import serializers
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    def create(self, contract):
        instance = Contract.objects.create(
            project=contract.get('project'),
            product=contract.get('product'),
            description=contract.get('description'),
            unit_price = contract.get('unit_price'),
            assignment = contract.get('assignment'),
            supplier = contract.get('supplier'),
            date = contract.get('date')
        )

        return instance

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.description = validated_data.get('description', instance.description)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.assignment = validated_data.get('assignment', instance.assignment)
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance

    class Meta:
        model = Contract
        fields = ['id', 'project', 'product', 'description', 'unit_price', 'assignment', 'supplier', 'date']
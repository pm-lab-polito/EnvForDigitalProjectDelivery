from rest_framework import serializers
from .models import Resource


class ResourceSerializer(serializers.ModelSerializer):    
    def create(self, data):
        resource = Resource.objects.create(
            project = data.get('project'),
            name = data.get('name'),
            description = data.get('description'),
            cost = data.get('cost'),
            category = data.get('category'),
        )
        return resource

    def update(self, instance, validated_data):
        if (validated_data.get('name') 
            or validated_data.get('description') 
            or validated_data.get('cost')
            or validated_data.get('category')): 

            instance.name = validated_data.get('name', instance.name)
            instance.description = validated_data.get('description', instance.description)
            instance.cost = validated_data.get('cost', instance.cost)
            instance.category = validated_data.get('category', instance.category)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({'detail':"At least, one attribute must be provided (name/description/cost/category)"})
       
    class Meta:
        model = Resource
        fields = ('id', 'project', 'name', 'description', 'cost', 'unit', 'category')
        
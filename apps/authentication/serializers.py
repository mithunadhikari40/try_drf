from abc import ABC, ABCMeta

from django.contrib import admin

from .models import Student

"""Extra validators, these can be used outside of serializers and can be reused as functions"""

from rest_framework import serializers

"""A simple validator which checks that the name should always starts with vowel letter"""


def start_with_vowel(val: str):
    if val is None:
        raise serializers.ValidationError('Name cannot be null')
    if val.__eq__(""):
        raise serializers.ValidationError('Name cannot be empty')
    if val[0].lower() not in ['a', 'e', 'i', 'o', 'u']:
        raise serializers.ValidationError('Name should start with a vowel letter.')
    return val


class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100, validators=[start_with_vowel])
    roll = serializers.IntegerField()
    city = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.roll = validated_data.get('roll', instance.roll)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance

    """Field level validation, Its syntax will be validate_ followed by field name
    We either raise an validation error or return that value, we can access the value in second parameter"""

    def validate_roll(self, value):
        """For now lets say roll cannot be greater than 20
        We can also access the current fields by self.name, self.city"""
        if value >= 200:
            raise serializers.ValidationError("All 200 seats are filled.")
        return value

    """Object level validation, Its syntax will be validate. We can access all the data in the second parameter
       We either raise an validation error or return that object, we can access the object in second parameter"""

    def validate(self, data):
        name = data.get('name')
        city = data.get('city')
        # roll = data.get('roll')
        # if roll >= 200:
        #     raise serializers.ValidationError("All 200 seats are filled.")

        if name.lower() == city.lower():
            raise serializers.ValidationError("Name and city cannot be same")
        return data

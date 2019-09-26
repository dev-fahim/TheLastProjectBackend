from menu.models import Menu
from rest_framework import serializers
from utils import get_main_user


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        exclude = ('main_user', )

    def create(self, validated_data):
        return Menu.objects.create(**validated_data, main_user=get_main_user(self.context['request'].user))

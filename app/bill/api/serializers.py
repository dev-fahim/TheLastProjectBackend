from rest_framework import serializers, status
from bill.models import BillData, Bill
from menu.models import Menu
from menu.api.serializers import MenuSerializer
from utils import get_main_user


class BillDataSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BillData
        exclude = ('bill', 'main_user')

    def validate(self, attrs):
        menu = Menu.objects.filter(main_user_id=get_main_user(self.context['request'].user))
        if attrs.get('menu') in menu:
            return attrs
        raise serializers.ValidationError(detail={}, code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_item(instance):
        return MenuSerializer(instance=instance.menu).data


class BillSerializer(serializers.ModelSerializer):

    bill_data = BillDataSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Bill
        exclude = ('main_user', )

    def create(self, validated_data):
        print(validated_data)
        bill_data = validated_data.pop('bill_data')
        bill = Bill.objects.create(**validated_data, main_user=get_main_user(self.context['request'].user))
        for i in bill_data:
            BillData.objects.create(**i, bill=bill, main_user=get_main_user(self.context['request'].user))
        return bill

    def update(self, instance, validated_data):
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()
        return instance

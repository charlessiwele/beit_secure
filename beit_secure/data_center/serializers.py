from rest_framework import serializers

from data_center.models import ClientTransaction


class ClientTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTransaction
        fields = [
            'transaction_type',
            'transaction_name',
            'transaction_description',
            'transaction_extra_info',
        ]

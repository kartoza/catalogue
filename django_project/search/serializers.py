# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import SearchRecord


class SearchRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for search record.
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = SearchRecord
        fields = [
            'pk',
            'user',
            'order',
            'product',
        ]

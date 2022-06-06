from rest_framework import serializers
from catalogue.models import OpticalProduct


class OpticalProductSerializer(serializers.ModelSerializer):
    """
    Serializer for optical product.
    """
    spatial_coverage = serializers.SerializerMethodField('get_spatial_coverage')
    product_name = serializers.SerializerMethodField('product_name')

    def get_spatial_coverage(self, obj):
        return obj.spatial_coverage.wkt

    def product_name(self, obj):
        return obj.product_name

    class Meta:
        model = OpticalProduct
        fields = '__all__'
        extra_fields = ['product_name']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(OpticalProductSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


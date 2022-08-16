from catalogue.models import VisitorReport
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class VisitSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = VisitorReport
        geo_field = "geometry"
        id_field = False
        fields = ('id', 'city', 'country', 'visit_count')

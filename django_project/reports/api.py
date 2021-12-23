from django.http import JsonResponse
from dictionaries.models import SatelliteInstrumentGroup
from django.db.models import Count
from rest_framework.views import APIView


class DataSummaryApiView(APIView):
    """Get data summary"""

    def get(self, request, *args):

        queryset = SatelliteInstrumentGroup.objects.annotate(
            id__count=Count(
                'satelliteinstrument__opticalproductprofile__opticalproduct')) \
            .order_by('satellite__name').filter(id__count__gt=0)

        all_json_data = []

        for result in queryset:
            json_data = dict()
            json_data['satellite_name'] = result.satellite.name
            json_data['instrument_type'] = result.instrument_type.name
            json_data['satellite_abbr'] = str(result.satellite.abbreviation)
            json_data['instrument_abbr'] = str(result.instrument_type.abbreviation)
            json_data['satellite_operator_abbr'] = str(result.satellite.operator_abbreviation)
            json_data['instrument_operator_abbr'] = str(result.instrument_type.operator_abbreviation)
            json_data['id__count'] = result.id__count
            try:
                json_data['min_year'] = result.min_year()
            except IndexError:
                json_data['min_year'] = '-'
            try:
                json_data['max_year'] = result.max_year()
            except IndexError:
                json_data['max_year'] = '-'
            all_json_data.append(json_data)

        return JsonResponse({"result": all_json_data})

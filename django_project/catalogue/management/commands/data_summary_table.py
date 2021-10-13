import json
from django.db.models import Count
from dictionaries.models import SatelliteInstrumentGroup
from django.core.management.base import BaseCommand

__author__ = 'rischan - <--rischan@kartoza.com-->, dimas - <--dimas@kartoza.com-->'
__date__ = '4/27/16'

halt_on_error = True


# dir_path=('/home/web/django_project/media/')


class Command(BaseCommand):
    args = 'path'
    help = 'Store data range data summary table from raw query'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        """Implementation for command

        :param args: path for the result files '/home/web/django_project/media/'
        :type args: str

        :raises: IOError

        """

        if options['path'] is None:
            self.stdout.write("Need argument for result path "
                              "ex : /home/web/django_project/media/")
            return

        path = options['path']

        file_name = 'output.json'

        try:
            json_file = open(path + file_name, 'w')
            json_file.seek(0)

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

            json_file.write(json.dumps(all_json_data, indent=4))
            json_file.truncate()
            json_file.close()

        except IOError:
            print('Error: can\'t find or read file')

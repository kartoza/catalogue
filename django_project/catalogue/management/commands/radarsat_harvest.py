from django.core.management.base import BaseCommand

from catalogue.ingestors import radarsat


class Command(BaseCommand):
	"""
	Tool for harvesting RADARSAT product XML files.
	"""

	help = 'Imports RADARSAT records into the SANSA catalogue'

	def add_arguments(self, parser):
		parser.add_argument(
			'--test_only',
			'-t',
			dest='test_only_flag',
			action='store_true',
			help='Just test, nothing will be written into the DB.',
			default=False)
		parser.add_argument(
			'--source_dir',
			'-d',
			dest='source_dir',
			action='store',
			help='Source directory containing RADARSAT product XML files.',
			default='/home/web/catalogue/django_project/Data_to_ingest/Radarsat2/')
		parser.add_argument(
			'--halt_on_error',
			'-e',
			dest='halt_on_error_flag',
			action='store',
			help='Halt on first error that occurs and print a stacktrace',
			default=False)
		parser.add_argument(
			'--ignore-missing-thumbs',
			'-i',
			dest='ignore_missing_thumbs_flag',
			action='store',
			help='Continue with import even if products are missing thumbnails.',
			default=True)

	@staticmethod
	def _parameter_to_bool(parameter):
		if isinstance(parameter, bool):
			return parameter
		return str(parameter).lower() == 'true'

	def handle(self, *args, **options):
		test_only = self._parameter_to_bool(options.get('test_only_flag'))
		source_dir = options.get('source_dir')
		verbose = int(options.get('verbosity'))
		halt_on_error = self._parameter_to_bool(
			options.get('halt_on_error_flag'))
		ignore_missing_thumbs = self._parameter_to_bool(
			options.get('ignore_missing_thumbs_flag'))

		radarsat.ingest(
			source_path=source_dir,
			test_only_flag=test_only,
			verbosity_level=verbose,
			halt_on_error_flag=halt_on_error,
			ignore_missing_thumbs=ignore_missing_thumbs)

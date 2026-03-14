import glob
import os
import shutil
from datetime import datetime
from xml.etree import ElementTree as ET

from django.conf import settings
from django.contrib.gis.geos import WKTReader
from django.core.management.base import CommandError
from django.db import transaction

from catalogue.models import RadarProduct
from dictionaries.models import (
	ImagingMode,
	InstrumentType,
	Projection,
	Quality,
	RadarProductProfile,
	Satellite,
	SatelliteInstrument,
	SatelliteInstrumentGroup,
)


def _parse_datetime(value):
	if not value:
		return None

	cleaned = value.strip()
	if cleaned.endswith('Z'):
		cleaned = cleaned[:-1]

	for pattern in (
		'%Y-%m-%dT%H:%M:%S.%f',
		'%Y-%m-%dT%H:%M:%S',
		'%Y-%m-%d %H:%M:%S',
	):
		try:
			return datetime.strptime(cleaned, pattern)
		except ValueError:
			continue

	return None


def _find_text(root, ns, xpath, default=None):
	element = root.find(xpath, ns)
	if element is None or element.text is None:
		return default
	return element.text.strip()


def _to_float(value, default=None):
	if value in (None, ''):
		return default
	try:
		return float(value)
	except (TypeError, ValueError):
		return default


def _to_int(value, default=None):
	if value in (None, ''):
		return default
	try:
		return int(float(value))
	except (TypeError, ValueError):
		return default


def _build_geometry(root, ns):
	latitudes = []
	longitudes = []

	for coordinate in root.findall('.//rs2:geodeticCoordinate', ns):
		latitude = _to_float(_find_text(coordinate, ns, 'rs2:latitude'))
		longitude = _to_float(_find_text(coordinate, ns, 'rs2:longitude'))
		if latitude is None or longitude is None:
			continue
		latitudes.append(latitude)
		longitudes.append(longitude)

	if not latitudes or not longitudes:
		raise CommandError('Could not build RADARSAT geometry from XML tie points.')

	min_lat = min(latitudes)
	max_lat = max(latitudes)
	min_lon = min(longitudes)
	max_lon = max(longitudes)
	polygon = (
		'POLYGON((' 
		f'{min_lon} {max_lat}, '
		f'{max_lon} {max_lat}, '
		f'{max_lon} {min_lat}, '
		f'{min_lon} {min_lat}, '
		f'{min_lon} {max_lat}'
		'))'
	)
	return WKTReader().read(polygon)


def _get_projection():
	projection = Projection.objects.filter(epsg_code='4326').first()
	if projection:
		return projection
	return Projection.objects.filter(name__icontains='WGS 84').first()


def _get_quality():
	quality = Quality.objects.filter(name__iexact='Unknown').first()
	if quality:
		return quality
	return Quality.objects.first()


def _first_or_none(queryset):
	return queryset.first()


def _resolve_product_profile(satellite_name, sensor_name, beam_mode, acquisition_type):
	satellite = _first_or_none(
		Satellite.objects.filter(operator_abbreviation__iexact=satellite_name)
	)
	if satellite is None:
		satellite = _first_or_none(
			Satellite.objects.filter(name__iexact=satellite_name)
		)
	if satellite is None:
		satellite = _first_or_none(
			Satellite.objects.filter(abbreviation__iexact=satellite_name)
		)

	if satellite is None:
		raise CommandError(
			f'No Satellite dictionary entry found for "{satellite_name}".'
		)

	instrument_type = _first_or_none(
		InstrumentType.objects.filter(operator_abbreviation__iexact=sensor_name)
	)
	if instrument_type is None:
		instrument_type = _first_or_none(
			InstrumentType.objects.filter(abbreviation__iexact=sensor_name)
		)
	if instrument_type is None:
		instrument_type = _first_or_none(
			InstrumentType.objects.filter(name__iexact=sensor_name)
		)
	if instrument_type is None:
		instrument_type = _first_or_none(
			InstrumentType.objects.filter(is_radar=True, name__icontains=sensor_name)
		)

	if instrument_type is None:
		raise CommandError(
			f'No InstrumentType dictionary entry found for "{sensor_name}".'
		)

	group = _first_or_none(
		SatelliteInstrumentGroup.objects.filter(
			satellite=satellite,
			instrument_type=instrument_type,
		)
	)
	if group is None:
		raise CommandError(
			'No SatelliteInstrumentGroup found for '
			f'satellite "{satellite}" and instrument "{instrument_type}".'
		)

	satellite_instrument = _first_or_none(
		SatelliteInstrument.objects.filter(satellite_instrument_group=group)
	)
	if satellite_instrument is None:
		raise CommandError(
			f'No SatelliteInstrument found for group "{group}".'
		)

	imaging_mode = None
	if beam_mode:
		imaging_mode = _first_or_none(
			ImagingMode.objects.filter(
				name__iexact=beam_mode,
				radarbeam__instrument_type=instrument_type,
			)
		)
	if imaging_mode is None and acquisition_type:
		imaging_mode = _first_or_none(
			ImagingMode.objects.filter(
				name__iexact=acquisition_type,
				radarbeam__instrument_type=instrument_type,
			)
		)
	if imaging_mode is None:
		imaging_mode = _first_or_none(
			ImagingMode.objects.filter(radarbeam__instrument_type=instrument_type)
		)

	if imaging_mode is None:
		raise CommandError(
			'No ImagingMode found for '
			f'instrument type "{instrument_type}". Add dictionary entries first.'
		)

	profile = _first_or_none(
		RadarProductProfile.objects.filter(
			satellite_instrument=satellite_instrument,
			imaging_mode=imaging_mode,
		)
	)
	if profile is None:
		profile = _first_or_none(
			RadarProductProfile.objects.filter(
				satellite_instrument=satellite_instrument
			)
		)

	if profile is None:
		raise CommandError(
			'No RadarProductProfile found for '
			f'satellite instrument "{satellite_instrument}".'
		)

	return profile


def _map_look_direction(value):
	if not value:
		return None
	value = value.lower()
	if value.startswith('l'):
		return 'L'
	if value.startswith('r'):
		return 'R'
	return None


def _map_orbit_direction(value):
	if not value:
		return None
	value = value.lower()
	if value.startswith('a'):
		return 'A'
	if value.startswith('d'):
		return 'D'
	return None


def _map_polarising_mode(polarisation_tokens):
	count = len(polarisation_tokens)
	if count <= 1:
		return 'S'
	if count == 2:
		return 'D'
	return 'Q'


def _find_thumbnail_file(base_dir):
	for pattern in ('*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG'):
		candidates = sorted(glob.glob(os.path.join(base_dir, pattern)))
		if candidates:
			return candidates[0]
	return None


def _discover_product_xml_files(source_path):
	matches = set(glob.glob(os.path.join(source_path, '**', 'product.xml'), recursive=True))
	matches.update(glob.glob(os.path.join(source_path, '**', 'product.XML'), recursive=True))

	if os.path.isfile(source_path) and source_path.lower().endswith('.xml'):
		matches.add(source_path)

	return sorted(matches)


def ingest(
	test_only_flag=True,
	source_path='/home/web/catalogue/django_project/Data_to_ingest/Radarsat2/',
	verbosity_level=2,
	halt_on_error_flag=True,
	ignore_missing_thumbs=False
):
	def log_message(message, level=1):
		if verbosity_level >= level:
			print(message)

	log_message(
		'Running RADARSAT Importer with options:\n'
		f'Test Only: {test_only_flag}\n'
		f'Source Dir: {source_path}\n'
		f'Verbosity: {verbosity_level}\n'
		f'Halt on Error: {halt_on_error_flag}\n'
		f'Ignore Missing Thumbs: {ignore_missing_thumbs}\n'
		'------------------',
		2,
	)

	ingestor_version = 'RADARSAT ingestor version 1.0'
	record_count = 0
	updated_record_count = 0
	created_record_count = 0
	failed_record_count = 0

	xml_files = _discover_product_xml_files(source_path)
	log_message(f'Found {len(xml_files)} RADARSAT XML file(s).', 1)

	for xml_file in xml_files:
		record_count += 1
		log_message(f'Processing: {xml_file}', 2)

		try:
			tree = ET.parse(xml_file)
			root = tree.getroot()

			if root.tag.startswith('{'):
				namespace = root.tag.split('}')[0][1:]
			else:
				namespace = ''
			ns = {'rs2': namespace} if namespace else {}

			original_product_id = _find_text(root, ns, './/rs2:productId')
			if not original_product_id:
				raise CommandError('Missing productId in RADARSAT XML.')

			processing_time = _parse_datetime(
				_find_text(root, ns, './/rs2:processingTime')
			)
			acquisition_start = _parse_datetime(
				_find_text(root, ns, './/rs2:zeroDopplerTimeFirstLine')
			) or _parse_datetime(
				_find_text(root, ns, './/rs2:rawDataStartTime')
			)
			acquisition_end = _parse_datetime(
				_find_text(root, ns, './/rs2:zeroDopplerTimeLastLine')
			)

			if acquisition_start is None and processing_time is None:
				raise CommandError('Missing acquisition/processing time in RADARSAT XML.')

			product_date = processing_time or acquisition_start
			geometry = _build_geometry(root, ns)

			sampled_pixel_spacing = _to_float(
				_find_text(root, ns, './/rs2:sampledPixelSpacing'),
				default=0.0,
			)
			sampled_line_spacing = _to_float(
				_find_text(root, ns, './/rs2:sampledLineSpacing'),
				default=0.0,
			)
			spatial_resolution = (
				(sampled_pixel_spacing + sampled_line_spacing) / 2.0
				if sampled_pixel_spacing and sampled_line_spacing
				else sampled_pixel_spacing or sampled_line_spacing or 0.0
			)

			radiometric_resolution = _to_int(
				_find_text(root, ns, './/rs2:bitsPerSample'),
				default=0,
			)

			polarizations_raw = _find_text(root, ns, './/rs2:polarizations', default='')
			polarization_tokens = [
				token.strip() for token in polarizations_raw.replace(',', ' ').split() if token.strip()
			]
			band_count = len(polarization_tokens) if polarization_tokens else 1

			satellite_name = _find_text(root, ns, './/rs2:satellite', default='RADARSAT-2')
			sensor_name = _find_text(root, ns, './/rs2:sensor', default='SAR')
			beam_mode = _find_text(root, ns, './/rs2:beamModeMnemonic')
			acquisition_type = _find_text(root, ns, './/rs2:acquisitionType')

			product_profile = _resolve_product_profile(
				satellite_name=satellite_name,
				sensor_name=sensor_name,
				beam_mode=beam_mode,
				acquisition_type=acquisition_type,
			)

			look_direction = _map_look_direction(
				_find_text(root, ns, './/rs2:antennaPointing')
			)
			orbit_direction = _map_orbit_direction(
				_find_text(root, ns, './/rs2:passDirection')
			)

			receive_configuration = None
			if polarization_tokens:
				leading = polarization_tokens[0][0].upper()
				if leading in ('H', 'V'):
					receive_configuration = leading

			incidence_near = _to_float(
				_find_text(root, ns, './/rs2:incidenceAngleNearRange')
			)
			incidence_far = _to_float(
				_find_text(root, ns, './/rs2:incidenceAngleFarRange')
			)
			if incidence_near is not None and incidence_far is not None:
				incidence_angle = (incidence_near + incidence_far) / 2.0
			else:
				incidence_angle = incidence_near or incidence_far

			projection = _get_projection()
			quality = _get_quality()

			metadata_xml = ET.tostring(root, encoding='unicode')
			image_id = _to_int(_find_text(root, ns, './/rs2:imageId'))
			input_dataset_id = _to_int(_find_text(root, ns, './/rs2:inputDatasetId'))

			record_data = {
				'spatial_coverage': geometry,
				'projection': projection,
				'quality': quality,
				'original_product_id': original_product_id,
				'unique_product_id': original_product_id,
				'metadata': metadata_xml,
				'radiometric_resolution': radiometric_resolution,
				'band_count': band_count,
				'spatial_resolution_x': sampled_pixel_spacing,
				'spatial_resolution_y': sampled_line_spacing,
				'spatial_resolution': spatial_resolution,
				'product_acquisition_start': acquisition_start or product_date,
				'product_acquisition_end': acquisition_end,
				'product_date': product_date,
				'path': input_dataset_id,
				'row': image_id,
				'product_profile': product_profile,
				'imaging_mode': acquisition_type or beam_mode,
				'look_direction': look_direction,
				'antenna_receive_configuration': receive_configuration,
				'polarising_mode': _map_polarising_mode(polarization_tokens),
				'polarising_list': ','.join(polarization_tokens),
				'slant_range_resolution': sampled_pixel_spacing,
				'azimuth_range_resolution': sampled_line_spacing,
				'orbit_direction': orbit_direction,
				'calibration': _find_text(root, ns, './/rs2:productType'),
				'incidence_angle': incidence_angle,
			}

			date_stamp = datetime.today().strftime('%Y-%m-%d')

			existing = RadarProduct.objects.filter(
				original_product_id=original_product_id
			).first()
			if existing:
				product = existing
				record_data['ingestion_log'] = (
					f'{existing.ingestion_log}\n'
					f'{date_stamp} : {ingestor_version} - updating record'
				)
				for key, value in record_data.items():
					setattr(product, key, value)
				update_mode = True
			else:
				record_data['ingestion_log'] = (
					f'{date_stamp} : {ingestor_version} - creating record'
				)
				product = RadarProduct(**record_data)
				update_mode = False

			try:
				with transaction.atomic():
					product.save()

					if not test_only_flag:
						thumb_file = _find_thumbnail_file(os.path.dirname(xml_file))
						if thumb_file:
							output_dir = os.path.join(
								settings.THUMBS_ROOT,
								product.thumbnailDirectory(),
							)
							os.makedirs(output_dir, exist_ok=True)
							output_file = os.path.join(
								output_dir,
								f'{product.product_id}.jpg',
							)
							shutil.copyfile(thumb_file, output_file)
						elif not ignore_missing_thumbs:
							raise CommandError(
								f'No thumbnail found for {original_product_id} '
								f'under {os.path.dirname(xml_file)}.'
							)
					else:
						transaction.set_rollback(True)

				if update_mode:
					updated_record_count += 1
				else:
					created_record_count += 1

			except Exception:
				failed_record_count += 1
				if halt_on_error_flag:
					raise

		except Exception as e:
			failed_record_count += 1
			log_message(f'Error processing {xml_file}: {e}', 1)
			if halt_on_error_flag:
				raise

	print('===============================')
	print(f'Products Processed: {record_count}')
	print(f'Products Updated: {updated_record_count}')
	print(f'Products Imported: {created_record_count}')
	print(f'Products Failed: {failed_record_count}')
	print('===============================')

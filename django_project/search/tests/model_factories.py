from datetime import date
import factory

from ..models import Search, SearchDateRange, Clip, SearchRecord


class SearchF(factory.django.DjangoModelFactory):
    """
    Search model factory
    """
    FACTORY_FOR = Search

    user = factory.SubFactory('core.model_factories.UserF')
    geometry = (
        'POLYGON ((17.54 -32.05, 20.83 -32.41, 20.30 -35.17, 17.84 '
        '-34.65, 17.54 -32.05))')
    ip_position = None
    guid = None
    record_count = None
    deleted = False
    search_date = None

    k_orbit_path = None
    j_frame_row = None
    use_cloud_cover = False
    cloud_mean = 5
    band_count = None
    spatial_resolution = None
    sensor_inclination_angle_start = None
    sensor_inclination_angle_end = None

    @factory.post_generation
    def instrument_types(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for instrument_type in extracted:
                self.instrument_type.add(instrument_type)

    @factory.post_generation
    def satellites(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for satellite in extracted:
                self.satellite.add(satellite)

    @factory.post_generation
    def license_types(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for license_type in extracted:
                self.license_type.add(license_type)

    @factory.post_generation
    def spectral_groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for spectral_group in extracted:
                self.spectral_group.add(spectral_group)

    @factory.post_generation
    def processing_levels(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for processing_level in extracted:
                self.processing_level.add(processing_level)

    @factory.post_generation
    def collections(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for collection in extracted:
                self.collection.add(collection)


class SearchDateRangeF(factory.django.DjangoModelFactory):
    """
    SearchDateRange model factory
    """
    FACTORY_FOR = SearchDateRange

    search = factory.SubFactory(SearchF)
    start_date = date(2010, 07, 15)
    end_date = date(2012, 07, 15)


class ClipF(factory.django.DjangoModelFactory):
    """
    Clip model factory
    """
    FACTORY_FOR = Clip

    guid = None
    owner = factory.SubFactory('core.model_factories.UserF')
    image = 'zaSpot2mMosaic2009'
    geometry = (
        'POLYGON ((17.5400390625000000 -32.0595703125000000, '
        '20.8359375000000000 -32.4111328125000000, 20.3085937500000000 '
        '-35.1796875000000000, 17.8476562500000000 -34.6523437500000000, '
        '17.5400390625000000 -32.0595703125000000))'
    )
    status = 'submitted'
    result_url = 'http://example.com/unittest'


class SearchRecordF(factory.django.DjangoModelFactory):
    """
    SearchRecord model factory
    """
    FACTORY_FOR = SearchRecord

    user = factory.SubFactory('core.model_factories.UserF')
    order = factory.SubFactory('orders.tests.model_factories.OrderF')
    product = factory.SubFactory(
        'catalogue.tests.model_factories.GenericProductF')
    internal_order_id = None
    download_path = factory.Sequence(lambda n: "Download path // {}".format(n))
    product_ready = False
    cost_per_scene = 0.0
    rand_cost_per_scene = 0.0
    currency = factory.SubFactory(
        'core.model_factories.CurrencyF')
    processing_level = factory.SubFactory(
        'dictionaries.tests.model_factories.ProcessingLevelF')
    projection = factory.SubFactory(
        'dictionaries.tests.model_factories.ProjectionF')
    product_process_state = factory.SubFactory(
        'dictionaries.tests.model_factories.ProductProcessStateF')

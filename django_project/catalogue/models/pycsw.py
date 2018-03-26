from django.db import models


class PycswBase(models.Model):
    """
    Generic Imagery product, it is always a composite aggregated products
    see: signals, to set spatial_resolution defaults and average
    """
    identifier = models.CharField(
        help_text='Original product id',
        max_length=255,
        primary_key=True,
        unique=True)
    type_name = models.CharField(
        help_text=(
            'sensor type abbreviation'),
        max_length=255,
        null=True,
        blank=True)
    schema = models.CharField(
        help_text=(
            'schema'),
        max_length=255,
        null=True,
        blank=True)
    mdsource = models.CharField(
        help_text=(
            'MD source'),
        max_length=255,
        null=True,
        blank=True)
    insert_date = models.DateField()
    xml = models.CharField(
        help_text=(
            'XML'),
        max_length=255,
        null=True,
        blank=True)
    any_text = models.CharField(
        help_text=(
            'Any Text'),
        max_length=255,
        null=True,
        blank=True)
    language = models.CharField(
        help_text=(
            'Language'),
        max_length=255,
        null=True,
        blank=True)
    title = models.CharField(
        help_text=(
            'Title'),
        max_length=255,
        null=True,
        blank=True)
    abstract = models.CharField(
        help_text=(
            'Abstract'),
        max_length=255,
        null=True,
        blank=True)
    keywords = models.CharField(
        help_text=(
            'Keywords'),
        max_length=255,
        null=True,
        blank=True)
    keyword_type = models.CharField(
        help_text=(
            'Keyword Type'),
        max_length=255,
        null=True,
        blank=True)
    format = models.CharField(
        help_text=(
            'Format'),
        max_length=255,
        null=True,
        blank=True)
    source = models.CharField(
        help_text=(
            'Source'),
        max_length=255,
        null=True,
        blank=True)
    date = models.DateField()
    modified_date = models.DateField()
    type = models.CharField(
        help_text=(
            'Type'),
        max_length=255,
        null=True,
        blank=True)
    bounding_box = models.CharField(
        help_text=(
            'Bounding Box'),
        max_length=255,
        null=True,
        blank=True)
    crs = models.CharField(
        help_text=(
            'CRS'),
        max_length=255,
        null=True,
        blank=True)
    alternate_title = models.CharField(
        help_text=(
            'Alternate Title'),
        max_length=255,
        null=True,
        blank=True)
    revision_date = models.DateField()
    creation_date = models.DateField()
    publication_date = models.DateField()
    organization_name = models.CharField(
        help_text=(
            'Organization Name'),
        max_length=255,
        null=True,
        blank=True)
    security_constraints = models.CharField(
        help_text=(
            'Security Constraints'),
        max_length=255,
        null=True,
        blank=True)
    parent_identifier = models.CharField(
        help_text=(
            'Parent Identifier'),
        max_length=255,
        null=True,
        blank=True)
    topic_category = models.CharField(
        help_text=(
            'Topic Category'),
        max_length=255,
        null=True,
        blank=True)
    resource_language = models.CharField(
        help_text=(
            'Resource Language'),
        max_length=255,
        null=True,
        blank=True)
    geographic_description_code = models.CharField(
        help_text=(
            'Geographic Description Code'),
        max_length=255,
        null=True,
        blank=True)
    denominator = models.CharField(
        help_text=(
            'Denominator'),
        max_length=255,
        null=True,
        blank=True)
    distance_value = models.CharField(
        help_text=(
            'Distance Value'),
        max_length=255,
        null=True,
        blank=True)
    distance_uom = models.CharField(
        help_text=(
            'Distance UOM'),
        max_length=255,
        null=True,
        blank=True)
    temp_extent_begin = models.DateField()
    temp_extent_end = models.DateField()
    service_type = models.CharField(
        help_text=(
            'Service Type'),
        max_length=255,
        null=True,
        blank=True)
    service_type_version = models.CharField(
        help_text=(
            'Service Type Version'),
        max_length=255,
        null=True,
        blank=True)
    operation = models.CharField(
        help_text=(
            'Operation'),
        max_length=255,
        null=True,
        blank=True)
    coupling_type = models.CharField(
        help_text=(
            'Coupling Type'),
        max_length=255,
        null=True,
        blank=True)
    operates_on = models.CharField(
        help_text=(
            'Operates On'),
        max_length=255,
        null=True,
        blank=True)
    operates_on = models.CharField(
        help_text=(
            'Operates On'),
        max_length=255,
        null=True,
        blank=True)
    operates_on_identifier = models.CharField(
        help_text=(
            'Operates On Identifier'),
        max_length=255,
        null=True,
        blank=True)
    operates_on_name = models.CharField(
        help_text=(
            'Operates On Name'),
        max_length=255,
        null=True,
        blank=True)
    degree = models.CharField(
        help_text=(
            'Degree'),
        max_length=255,
        null=True,
        blank=True)
    access_constraints = models.CharField(
        help_text=(
            'Access Constraints'),
        max_length=255,
        null=True,
        blank=True)
    other_constraints = models.CharField(
        help_text=(
            'Other Constraints'),
        max_length=255,
        null=True,
        blank=True)
    classification = models.CharField(
        help_text=(
            'Classification'),
        max_length=255,
        null=True,
        blank=True)
    condition_applying_to_access_and_use = models.CharField(
        help_text=(
            'Condition Applying To Access and Use'),
        max_length=255,
        null=True,
        blank=True)
    lineage = models.CharField(
        help_text=(
            'Lineage'),
        max_length=255,
        null=True,
        blank=True)
    responsible_party_role = models.CharField(
        help_text=(
            'Responsible Party Role'),
        max_length=255,
        null=True,
        blank=True)
    specification_title = models.CharField(
        help_text=(
            'Specification Title'),
        max_length=255,
        null=True,
        blank=True)
    # specification_date = models.DateField()
    specification_date_type = models.CharField(
        help_text=(
            'Specification Date type'),
        max_length=255,
        null=True,
        blank=True)
    creator = models.CharField(
        help_text=(
            'Creator'),
        max_length=255,
        null=True,
        blank=True)
    publisher = models.CharField(
        help_text=(
            'Publisher'),
        max_length=255,
        null=True,
        blank=True)
    contributor = models.CharField(
        help_text=(
            'Contributor'),
        max_length=255,
        null=True,
        blank=True)
    relation = models.CharField(
        help_text=(
            'Relation'),
        max_length=255,
        null=True,
        blank=True)
    links = models.CharField(
        help_text=(
            'Links'),
        max_length=255,
        null=True,
        blank=True)

    objects = models.Manager()

    class Meta:
        abstract = True
        app_label = 'catalogue'

    def getMetadataDict(self):
        """
        Returns metadata dictionary
        """
        metadata = dict(
            identifier=self.identifier,
            type_name=self.type_name,
            schema=self.schema,
            mdsource=self.mdsource,
            insert_date=self.insert_date,
            xml='',
            any_text='',
            language=self.language(),
            title='',
            abstract='',
            keywords='',
            keyword_type='',
            format=self.format,
            source='',
            date=self.date,
            modified_date=self.modified_date,
            type='',
            bounding_box=self.bounding_box,
            crs=self.crs,
            alternate_title='',
            revision_date=self.revision_date,
            creation_date=self.creation_date,
            publication_date='',
            organization_name=self.organization_name,
            security_constraints='',
            parent_identifier='',
            topic_category='',
            resource_language='',
            geo_desc_code='',
            denominator='',
            distance_value='',
            distance_uom='',
            temp_extent_begin='',
            temp_extent_end='',
            service_type='',
            service_type_version='',
            operation='',
            coupling_type='',
            operates_on='',
            operates_on_identifier='',
            operates_on_name='',
            degree='',
            access_constraints='',
            other_constraints='',
            classification='',
            condition_applying_tau='',
            lineage='',
            responsible_party_role='',
            spec_title='',
            # spec_date='',
            spec_date_type='',
            creator=self.creator,
            publisher=self.publisher,
            contributor='',
            relation='',
            links=self.links,)
        return metadata


# The use of the three classes below is for administering each satellite
# For a single metadata for all satellite, use PycswExtraFields class
class PycswCbers(PycswBase):
    pass


class PycswLandsat(PycswBase):
    pass


class PycswSpot(PycswBase):
    pass


# Use this class for one table metadata
# Otherwise, use Pycsw<Satellite> class
class PycswExtraFields(PycswBase):
    sensor_abbreviation = models.CharField(
        help_text=(
            'Field to query to Dictionary_InstrumentType table using operator_abbreviation column'),
        max_length=255,
        null=True,
        blank=True)
    satellite_abbreviation = models.CharField(
        help_text=(
            'Field to query to Dictionary_Satellite table using abbreviation column'),
        max_length=255,
        null=True,
        blank=True)

    def getMetadataDict(self):
        """
        Returns metadata dictionary
        """
        super(PycswExtraFields, self).getMetadataDict()
        metadata = dict(
            sensor_abbreviation=self.sensor_abbreviation,
            satellite_abbreviation=self.satellite_abbreviation,)
        return metadata

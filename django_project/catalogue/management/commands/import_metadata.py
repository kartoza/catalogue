from datetime import datetime

from dictionaries.models import SatelliteInstrumentGroup
from django.core.management.base import BaseCommand
from django.db import connection, IntegrityError


class Command(BaseCommand):
    help = 'Import data to pycsw table'

    def handle(self, *args, **options):
        """ command execution """

        satellite = SatelliteInstrumentGroup.objects.all()

        with connection.cursor() as cursor:
            for ins in satellite:
                ins_type = "Optical"
                if ins.instrument_type.is_radar:
                    ins_type = "Radar"
                try:
                    cursor.execute("INSERT INTO records("
                                   "identifier, "
                                   "typename, "
                                   "schema, "
                                   "mdsource, "
                                   "insert_date, "
                                   "xml, "
                                   "anytext, "
                                   # "metadata, "
                                   "metadata_type, "
                                   # "language, "
                                   # "type, "
                                   "title, "
                                   # "title_alternate, "
                                   # "abstract, "
                                   "keywords, "
                                   # "keywordstype, "
                                   # "parentidentifier, "
                                   # "relation, "
                                   # "time_begin, "
                                   # "time_end, "
                                   # "topicategory, "
                                   # "resourcelanguage, "
                                   # "creator, "
                                   # "publisher, "
                                   # "contributor, "
                                   # "organization, "
                                   # "securityconstraints, "
                                   # "accessconstraints, "
                                   # "otherconstraints, "
                                   "date, "
                                   # "date_revision, "
                                   # "date_creation, "
                                   # "date_publication, "
                                   # "date_modified, "
                                   # "format, "
                                   # "source, "
                                   # "crs, "
                                   # "geodescode, "
                                   # "denominator, "
                                   # "distancevalue, "
                                   # "distanceuom, "
                                   # "wkt_geometry, "
                                   # "servicetype, "
                                   # "servicetypeversion, "
                                   # "operation, "
                                   # "couplingtype, "
                                   # "operateson, "
                                   # "operatesonidentifier, "
                                   # "operatesoname, "
                                   # "degree, "
                                   # "classification, "
                                   # "conditionapplyingtoaccessanduse, "
                                   # "lineage, "
                                   # "responsiblepartyrole, "
                                   # "specificationtitle, "
                                   # "specificationdate, "
                                   # "specificationdatetype, "
                                   # "platform, "
                                   "instrument, "
                                   "sensortype, "
                                   # "cloudcover, "
                                   "bands)"
                                   # "links, "
                                   # "anytext_tsvector, "
                                   # "wkb_geometry)"
                                   "VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ",
                                   (ins.satellite.name,
                                    'pycsw:CoreMetadata',
                                    "http://www.opengis.net/cat/csw/2.0.2",
                                    "local",
                                    '', '', '',
                                    ins.satellite.launch_date.strftime("%m/%d/%y"),
                                    ins.satellite.name,
                                    ins.instrument_type.keywords,
                                    datetime.now().strftime("%m/%d/%y"),
                                    ins.instrument_type.name,
                                    ins_type,
                                    str(ins.instrument_type.band_count),)
                                   )
                except IntegrityError:
                    cursor.execute("UPDATE records SET "
                                   "identifier=%s, "
                                   "typename=%s, "
                                   "schema=%s, "
                                   "mdsource=%s, "
                                   "insert_date=%s, "
                                   "xml=%s, "
                                   "anytext=%s, "
                                   # "metadata, "
                                   "metadata_type=%s, "
                                   # "language, "
                                   # "type, "
                                   "title=%s, "
                                   # "title_alternate, "
                                   # "abstract, "
                                   "keywords=%s, "
                                   # "keywordstype, "
                                   # "parentidentifier, "
                                   # "relation, "
                                   # "time_begin, "
                                   # "time_end, "
                                   # "topicategory, "
                                   # "resourcelanguage, "
                                   # "creator, "
                                   # "publisher, "
                                   # "contributor, "
                                   # "organization, "
                                   # "securityconstraints, "
                                   # "accessconstraints, "
                                   # "otherconstraints, "
                                   "date=%s, "
                                   # "date_revision, "
                                   # "date_creation, "
                                   # "date_publication, "
                                   # "date_modified, "
                                   # "format, "
                                   # "source, "
                                   # "crs, "
                                   # "geodescode, "
                                   # "denominator, "
                                   # "distancevalue, "
                                   # "distanceuom, "
                                   # "wkt_geometry, "
                                   # "servicetype, "
                                   # "servicetypeversion, "
                                   # "operation, "
                                   # "couplingtype, "
                                   # "operateson, "
                                   # "operatesonidentifier, "
                                   # "operatesoname, "
                                   # "degree, "
                                   # "classification, "
                                   # "conditionapplyingtoaccessanduse, "
                                   # "lineage, "
                                   # "responsiblepartyrole, "
                                   # "specificationtitle, "
                                   # "specificationdate, "
                                   # "specificationdatetype, "
                                   # "platform, "
                                   "instrument=%s, "
                                   "sensortype=%s, "
                                   # "cloudcover, "
                                   "bands=%s",
                                   # "links, "
                                   # "anytext_tsvector, "
                                   "wkb_geometry=%s",
                                   (ins.satellite.name,
                                    'pycsw:CoreMetadata',
                                    "http://www.opengis.net/cat/csw/2.0.2",
                                    "local",
                                    '', '', '',
                                    ins.satellite.launch_date.strftime("%m/%d/%y"),
                                    ins.satellite.name,
                                    ins.instrument_type.keywords,
                                    datetime.now().strftime("%m/%d/%y"),
                                    ins.instrument_type.name,
                                    ins_type,
                                    str(ins.instrument_type.band_count),)
                                   )


            cursor.fetchone()

from django.contrib.gis.utils import LayerMapping
from django_project.catalogue.models.others import WorldBorders,world_borders_mapping

SHAPE_FILE='resources/world_borders/TM_WORLD_BORDERS-0.3.shp'

lm = LayerMapping(WorldBorders, SHAPE_FILE, world_borders_mapping,encoding='latin-1')

lm.save()

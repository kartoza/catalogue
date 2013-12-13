"""
SANSA-EO Catalogue - Catalogue admin interface

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '01/01/2011'
__copyright__ = 'South African National Space Agency'

from django.contrib.gis import admin

from .models import (
    ProcessingLevel,
    Collection,
    Satellite,
    ScannerType,
    InstrumentType,
    RadarBeam,
    ImagingMode,
    SatelliteInstrumentGroup,
    SatelliteInstrument,
    Band,
    SpectralGroup,
    SpectralMode,
    BandSpectralMode,
    InstrumentTypeProcessingLevel,
    SpectralModeProcessingCosts,
    OpticalProductProfile,
    RadarProductProfile,
    ForeignCurrency,
    ReferenceSystem
)


####################################
# New Dictionaries
####################################

class ProcessingLevelAdmin(admin.ModelAdmin):
    search_fields = ['name', 'abbreviation', 'description']
    list_display = ['name', 'abbreviation', 'description']
admin.site.register(ProcessingLevel, ProcessingLevelAdmin)


class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['name', 'institution', 'description']
    list_display = ['name', 'institution', 'description']
admin.site.register(Collection, CollectionAdmin)


class SatelliteAdmin(admin.ModelAdmin):
    search_fields = ['name', 'abbreviation', 'description']
    list_filter = [
        'launch_date',
        'revist_time_days',
        'status',
        'license_type']
    list_display = ['name', 'abbreviation', 'description']
admin.site.register(Satellite, SatelliteAdmin)


class ScannerTypeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'abbreviation', 'description']
    list_display = ['name', 'abbreviation', 'description']
admin.site.register(ScannerType, ScannerTypeAdmin)


class InstrumentTypeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'abbreviation', 'description']
    list_display = [
        'name',
        'abbreviation',
        'description',
        'is_radar',
        'band_count',
        'pixel_size_list_m',
        'spatial_resolution_range',
        'image_size_km']
admin.site.register(InstrumentType, InstrumentTypeAdmin)


class RadarBeamAdmin(admin.ModelAdmin):
    list_display = [
        'instrument_type',
        'band_name',
        'wavelength_cm',
        'looking_distance',
        'azimuth_direction']
    pass
admin.site.register(RadarBeam, RadarBeamAdmin)


class ImagingModeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = [
        'name',
        'incidence_angle_min',
        'incidence_angle_max',
        'approximate_resolution_m',
        'swath_width_km',
        'number_of_looks',
        'polarization']
admin.site.register(ImagingMode, ImagingModeAdmin)


class SatelliteInstrumentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'abbreviation', 'description']
    list_filter = ['satellite_instrument_group']
    list_display = [
        'name',
        'abbreviation',
        'description',
        'satellite_instrument_group']
admin.site.register(SatelliteInstrument, SatelliteInstrumentAdmin)


class SatelliteInstrumentGroupAdmin(admin.ModelAdmin):
    list_filter = ['satellite', 'instrument_type']
    list_display = ['satellite', 'instrument_type']
admin.site.register(SatelliteInstrumentGroup, SatelliteInstrumentGroupAdmin)


class BandAdmin(admin.ModelAdmin):
    search_fields = ['band_name']
    list_filter = ['instrument_type']
    list_display = ['instrument_type', 'band_name', 'band_abbr']
admin.site.register(Band, BandAdmin)


class SpectralGroupAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ['abbreviation', 'name', 'description']
admin.site.register(SpectralGroup, SpectralGroupAdmin)


class SpectralModeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_filter = ['instrument_type', 'spectralgroup']
    list_display = [
        'abbreviation',
        'name',
        'instrument_type',
        'spectralgroup',
        'description']
admin.site.register(SpectralMode, SpectralModeAdmin)


class BandSpectralModeAdmin(admin.ModelAdmin):
    list_filter = ['spectral_mode']
    list_display = ['spectral_mode', 'band']
admin.site.register(BandSpectralMode, BandSpectralModeAdmin)


class InstrumentTypeProcessingLevelAdmin(admin.ModelAdmin):
    list_filter = ['instrument_type', 'processinglevel']
    list_display = [
        'instrument_type',
        'processinglevel',
        'operator_processing_level_name',
        'operator_processing_level_abbreviation']
admin.site.register(
    InstrumentTypeProcessingLevel, InstrumentTypeProcessingLevelAdmin)


class SpectralModeProcessingCostsAdmin(admin.ModelAdmin):
    list_filter = ['spectral_mode']
    list_display = [
        'spectral_mode',
        'instrumenttypeprocessinglevel',
        'cost_per_scene_in_rands',
        'foreign_currency',
        'cost_per_scene_in_foreign']
admin.site.register(
    SpectralModeProcessingCosts, SpectralModeProcessingCostsAdmin)


class OpticalProductProfileAdmin(admin.ModelAdmin):
    list_filter = ['satellite_instrument', 'spectral_mode']
    list_display = ['satellite_instrument', 'spectral_mode']
admin.site.register(OpticalProductProfile, OpticalProductProfileAdmin)


class RadarProductProfileAdmin(admin.ModelAdmin):
    list_filter = ['satellite_instrument', 'imaging_mode']
    list_display = ['satellite_instrument', 'imaging_mode']
admin.site.register(RadarProductProfile, RadarProductProfileAdmin)


class ForeignCurrencyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['abbreviation', 'name', 'conversion_rate']
admin.site.register(ForeignCurrency, ForeignCurrencyAdmin)


class ReferenceSystemAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ['abbreviation', 'name', 'description']
admin.site.register(ReferenceSystem, ReferenceSystemAdmin)

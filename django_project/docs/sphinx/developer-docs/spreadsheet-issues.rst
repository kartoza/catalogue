= issues with the dictionaries provided by Wolfgang =

- NOAA missions have no matching sensors except for NOAA-14

- The concept of Acquisition Mode and Sensor typed have been switched. E.g. in the api notes I made with Wolfgang in attendance I documented:

```
 61 class SensorType( models.Model ):
 62   """Sensor type / camera number e.g. CAM1"""
 63   abbreviation = models.CharField( max_length="4")
 64   name = models.CharField( max_length="255" )
 65   mission_sensor = models.ForeignKey(MissionSensor ) # e.g. HRV
 66   is_taskable = models.BooleanField(default=True)
 67   operator_abbreviation = models.CharField( max_length=255 ) # UI abbreviation
 68   class Meta:
 69     app_label= 'catalogue'
 70     unique_together = ('mission_sensor', 'abbreviation')
 71   def __unicode__(self):
 72     return "%s:%s" % (self.mission_sensor.operator_abbreviation, self.name)
 73             
 74 ###############################################################################
 75           
 76 class AcquisitionMode( models.Model ):
 77   """Acquisition mode.
 78      @note: mode examples:
 79            J = Multispectral 10m
 80            P/M = Panchromatic 10m
 81            A/B = Panchromatic 5m
 82            T = Panchromatic 2.5m
 83            X = Multispectral 20m
 84            JT = Pansharpened 2.5m Multispectral"""
 85   sensor_type = models.ForeignKey(SensorType ) #e.g. CAM1
  86   abbreviation = models.CharField( max_length="4")
 87   name = models.CharField( max_length="255" )
 88   spatial_resolution = models.IntegerField(help_text="Spatial resolution in m")
 89   band_count = models.IntegerField()
 90   is_grayscale = models.BooleanField(default=False)
 91   operator_abbreviation = models.CharField( max_length=255 ) # UI abbreviation
 92   class Meta: 
 93     app_label= 'catalogue'
 94     unique_together = ('sensor_type', 'abbreviation')
 95   def __unicode__(self):
 96     return "%s:%s" % (self.sensor_type.mission_sensor.operator_abbreviation, self.name)
 97           
 98           

```

- The properties of resolution and bands, (and probably grayscale) have been also switched out to type - this breaks all our triggers and logic through the app





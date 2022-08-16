
New Dictionaries
================

A description of the SANSA new dictionaries for
Generic Sensor Based Products

Overview
--------

The new dictionaries describe the relationships between the entities which describe the
products presented in the online catalogue. Each satellite imagery product has unique
characteristics based on the sensor and the information from the dictionaries is used for
searching the product list or to provide a detailed summary or fact sheet.

Institution
-----------

The owner of the satellite is the institution which is responsible for the acquisition of the
imagery or products. An institution may own many satellites with different sensors for
imagery acquisition, eg. Astium, USGS.

Collection
----------

A collection of satellites have a similar name and form a series usually with a sequential
number, eg. Landsat, SPOT, CBERS. A collection has a single owner.

License
-------

Satellite imagery is distributed by SANSA under licence issued by the owner or institution.
The SANSACommercial License allows for the sale of imagery to customers with free
distribution in limited quantities to researchers and unlimited distribution to partner
government departments, eg. Landsat, SPOT and ERS (radar) imagery. Free data can
be ordered and downloaded immediately via a link on an order confirmation email, eg.
SumbandilaSat, CBERS-2B and SAC-C imagery. The Partner License is no longer applied
separately, but included in the Commercial Licence. The licence agreement is applied to
each satellite.

Satellite
---------

The satellite is the spacecraft on which the sensors are borne. The satellite mission belongs
to a collection of satellites and is identified by the satellite name and a series number (if
there is more than one satellite in the collection), eg. Landsat 7, SPOT 5. The attributes of
a satellite include the launch date, the orbit description, revisit time, altitude and the current
status of the spacecraft. A satellite may have more than one sensor on board, each with their
unique characteristics.

Satellite Instrument
--------------------

The instruments or sensors carried on board a satellite or spacecraft are unique to the satellite
and are described by the Instrument Type. Most satellites carry a single camera or sensor of a
similar Instrument Type. SPOT satellites carry a duplicate of the sensor described as Camera
1 and Camera 2. For this reason the Satellite Instrument information distinguishes duplicate
sensors if applicable. A satellite may carry one or many different Instrument Types on board.

Instrument Type
---------------

A sensor or camera has typical characteristics which may be common to more than one
satellite in the collection. It is not uncommon for the same sensor design to be repeated and
launched on successive satellites for continuity of acquisitions over the lifespan of more
than one satellite, eg. Landsat MSS sensor on Landsat 1, 2, 3 and 4; SPOT HRV sensor on
SPOT 1, 2 and 3. The attributes of the sensor or instrument type remain constant, but there
maybe one or more instruments of the same type in orbit. Instruments are optical or radar
sensors with different characteristics giving rise to a split in the relevant attributes: optical
instruments have band and spectral mode attributes, while radar instruments have beam and
imaging mode attributes.

Scanner Type
------------

The sensor scans along the path of the satellite orbit using different methods for acquisition,
eg. Whisk Broom, Push Broom, Active Beam or Forward Motion Compensation. The design
of the sensor defines the scanner type or method used and is unique for each Instrument
Type.

Radar Beam
----------

A radar beam is an active scanner measuring the backscatter of the beam.

Imaging Mode
------------

A radar beam has one or more imaging modes, eg. wavelength, polarization.

Band
----

The electromagnetic spectrum wavelength ranges measured by the detectors on the sensor
are defined as spectral bands. The bands range from the visible spectrum, near infra-red,
short wave infra-red to thermal infra-red bands. A panchromatic range may include only
the visible wavelengths or include the near infra-red wavelengths. Each Instrument Type
has a defined wavelength range for each band expressed in nanometres (nm). The band
combinations for the satellite Instrument Type give a product or spectral mode, eg. Landsat
7 multispectral product of the visible, near infra-red and shortwave infra-red bands (HRF);
SPOT 5 panchromatic super-sampled product (T); CBERS-2B 5 band multispectral and
panchromatic bands (5BF).

Spectral Group
--------------

A generalised grouping of all imagery from optical sensors used for searching for products
with similar spectral characteristics, eg. panchromatic, multispectral, RGB, hyperspectral,
stereo pairs.

Spectral Mode
-------------

The spectral group applicable to each Instrument Type and the typical name or abbreviation
used to denote the spectral grouping.

Band Spectral Mode
------------------

The link between the bands and the spectral modes for the Instrument Types which details
each band the makes up the spectral group for that sensor, eg. Landsat 5 multi-spectral is
the blue, green, red, near infra-red and shortwave infra-red band combination; SPOT 5
multispectral is the green, red, near infra-red and shortwave infra-red band combination.

Processing Level
----------------

Imagery products acquired from the owner or institution either by download from the satellite
or by bulk delivery on disc or ftp are received at a base or starting processing level. Further
processing by SANSA may be an option for some imagery. The processing levels offered by
SANSA are specific to different Instrument Types. The conventional processing terminology
is applied as follow: Level 1A Radiometric correction, Level 1B Geometric correction, Level
2A Projected, Level 2B Geolocated with GCPs, Level 3Aa Orthorectified, Level 3Ab at
sensor reflectance, Level 4 Value added products. Provision is made for the original supplier
processing level naming to be displayed to assist the user to understand the processing level
required.

InstrumentTypeProcessingLevel
-----------------------------

Each Instrument Type has appropriate processing levels available for request. Not all
processing levels are available for every product, depending on the base processing level at
which the imagery was received by SANSA and the processing ability for some imagery is
limited.

Spectral Mode Processing Costs
------------------------------

Processing of imagery has costs associated with each level and what spectral mode or group
of bands is to be processed. The inclusion of costs linked to the processing levels and bands
allows for cost estimates to be calculated at the time of order request.

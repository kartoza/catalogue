

% Leave the blank space above here

== Introduction ==

**Note:** This section is intended to provide context for the impetus for 
the development of the catalogue system to third party developers.

=== The CSIR ===
This project has been carried out for the erstwhile CSIR Satellite Applications Center,
near Johannesburg, South Africa. The CSIR is the 'Council for Science and
Industrial Research' - it is the main national science foundation of the
country. The CSIR is a large organisation with many divisions of which SAC
(Satellite Applications Center) was one. SAC has since been incoporated into 
the South African National Space Agency (as described below).

=== SAC ===
SAC is a satellite ground station. This means they have a big campus with many
antennas and collect information from satellites as they pass over our sky
window they also do satellite tasking (telling satellites where to go and what
to do) and satellite / space craft telemetry (tracking space vehicle orbit
information etc).

SAC has two divisions:
 + Telemetry command and control where they do tracking, tasking etc.
 + EO (Earth Observation) where the focus is more software based to do remote
   sensing and generate products from imagery downloaded from satellites
 +

SAC-EO is the client for this project.

=== SANSA Takover ===

South Africa is busy creating its own space agency - SANSA (South AfricAN
National Space Agency). SANSA will aggregate space technology from various gov,
parastatal, non-gov organisations to form a new organisation funded by the
state.  SAC-EO became part of SANSA as of 1 April 2011 and will and is now SANSA-EO.

=== The project ===

SAC-EO has been building for the last 3 or 4 years an integrated system before
this project (of which we form a small part), the processing of imagery was
done manually and ad-hoc which is not very efficient and prone to difficulty if
an expert leaves.

Thus they have started to build an integrated system called SAEOS (pronounced
'sigh-os').  The purpose of SAEOS is to create an automated processing
environment through all the steps of the EO product workflow i.e.:

 - satellite tasking ('please programme spot5 to take an image at footprint foo on date X')
 - image processing (level 1a through 3a/b)
 - image analysis (level 4)
 - image ordering ('can I please get a copy of that SPOT image you took on dec 4 2008 of this area')
 - product packaging ('bundle up the stuff that was ordered using a DVD robot,
   placing on an ftp site, writing to an external HD etc')
 - 

To achieve this goal they have a number of software components.

The first components are the 'terminal software'. Terminal software are
provided by satellite operators such as SPOT5 (I will use SPOT as an example a
lot as its the pilot sensor for their project, eventually to incorporate many
more sensors) The terminal software is typically a linux box with the operators
own proprietary software on top that lets the operators do the tasking of
satellites (to collect an image at a given place and time) and also to extract
archived images from their tape library

The second component is 'SARMES'. SARMES is a collection of EASI scripts /
routines.  EASI is a programming language that runs on top of PCI / Geomatica a
proprietary GIS tool that runs on windows and linux. SAC are busy porting SARMES to
SARMES II which has the same functionality but uses python language bindings of
PCI/Geomatica instead of EASI script. SARMES has all the logic to do things like:

 - take a raw image and convert it to a common GIS format e.g. pix, gtiff etc.
 - collect GCP's automatically using a reference image
 - orthorectify an image using a dem, gcps and other reference data
 - reproject the image into different coord systems (typically UTM 33S - UTM
   36S in our area but others may apply too)
 - perform atmospheric correction to remove effects of the stratosphere
   interference between lens and ground target
 - perform sensor specific correction to e.g. remove effects of lens distortion
   on a specific camera (using published sensor models)
 - perform mosaicking of images to create one big seamless colour corrected
   dataset
 - perform pan sharpening (make a colour image higher resolution by merging it
   with a pan-chromatic / grey scale band)
 - chop up images in various tile schemes (e.g. degree squares, quarter degree
   sqauares etc)
 -

These jobs are run by manual process - creating config files, placing input
files in a specific dir heirachy etc.

The third component is DIMS. DIMS is a software system running on top of linux
written in java, corba, and using oracle or postgresql as a backend (at SAC
they are using PostgreSQL).  DIMS is proprietary software written by a german
company called WERUM. The same software is used by the German Space Agency and
others. DIMS provides automated tool chain processing. Basically you set up work flows
and run them using an 'operating tool'. Although DIMS uses postgresql, there is
no third party access to that db and the whole system should be considered a
black box except for a few specific entry and exit points.

DIMS is being extended and customised for SAC-EO including modifications so it
wll provide ogc interfaces.  Before this had their own catalogue implementation
and ordering system using very old standards or proprietary interfaces.  So
DIMS can process EO data and it builds up a catalogue of products that it has
processed or 'knows about' - in its own silo.  This catalogue is / will be
accessible via CSW and for processing of ordering they are implementing the OGC

The OS4EO (ordering service for earth observation) is an ogc standard. The
OS4EO standard is pretty simple and familiar. In essence it allows you to:
 - get capabilities
 - get quote
 - place order
 -

In DIMS it is implemented using SOAP rather than a RESTful service.

Along the process of creating the SAEOS project, SAC-EO have also been
investing in high end hardware - particularly storage.  They have a petabyte
capable heirachical storage system that in short works as follows:

 - data is written to local hard drives
 - after a certain period of inactivity moved down to slower sata drives (nearline storage)
 - and after that its migrated down onto a tape library
 -
 
The tape library (offline storage) is treated as part of the file system. It
has a robot arm that loads tapes automatically. When you browse the file
system, it appears that all data is local since all inodes are present in
online storage. When you try to read a file that is offline, the robot fetches
if from tape and puts it online - typically in under a minute, though that 
depends on system load.

DIMS is integrated with this file system (this file system is SGI's HFS -
Heirachical File System).  HFS is also proprietary software running on top of
Linux. One of the things DIMS will be doing is de-archiving from old manually
loaded tapes and moving them into HFS.  De-archiving historically collected raw
satellite imagery that is.  When DIMS is finished going through that there will
be hundreds of thousands (probably millions) of raw images stored in HFS and
accessible via DIMS. 

Since DIMS integrates with SARMES so you can do things like:

"Pull out that landsat 5 image from 2002, orthorectify it, correcto for
atmospheric interference and lens distortions, reproject it to UTM 35S and clip
it to this bounding box, then place the product on a dvd and write this label
on it"

Thats the goal of the system - end to end automation with minimal operator
intervention.

=== The Online Catalogue ===

Along side of these other packages, Linfiniti has been building a new web
catalogue for SAC-EO.  The catalogue is django + postgresql + all the other
great FOSS tools we can use together to make a rich, interactive site.

The Online catalogue has the capability to deliver some products directly if
they are held on local storage and also some basic capabilities for visitors to
submit tasking requests.

The purpose of this document is to provide technical detail covering the setup and 
deployment of the catalogue, as well as an architectural overview. API documentation 
is provided as a separate, complementary document to this one.

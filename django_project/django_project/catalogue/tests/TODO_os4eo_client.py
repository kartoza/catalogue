"""

os4eo WS client tests

>>> from catalogue.os4eo_client import OS4EOClient
>>> os4eo = OS4EOClient(debug=False)

>>> os4eo.GetCapabilities()
[<Element '{http://www.opengis.net/ows}Operation' ...

Place single order

>>> single_id, single_submit_status = os4eo.Submit( \
  ['SPOT5.HRG.L1A:/eods_hb_pl_eods_XXXXB00000000253027605285/eods_hb_pl_eods_//SPOT5.HRG.L1A'], \
  '100001', \
)

Place multiple

>>> multiple_id, multiple_submit_status = os4eo.Submit( \
  ['SPOT5.HRG.L1A:/eods_hb_pl_eods_XXXXB00000000253027605285/eods_hb_pl_eods_//SPOT5.HRG.L1A', \
  'SPOT5.HRG.L1A:/eods_hb_pl_eods_XXXXB00000000253027605866/eods_hb_pl_eods_//SPOT5.HRG.L1A' ], \
  '100002', \
)

>>> single_id
'urn:EOP:SAC:EOWEB...'

>>> multiple_id
'urn:EOP:SAC:EOWEB...'

>>> os4eo.GetStatus(single_id)
'Submitted'

>>> os4eo.GetStatus(multiple_id)
'Submitted'

>>> os4eo.GetStatus(single_id, True)
'Submitted'

>>> os4eo.GetStatus(multiple_id, True)
'Submitted'

>>> os4eo.DescribeResultAccess(single_id)
'failure'

>>> os4eo.DescribeResultAccess(multiple_id)
'failure'
"""

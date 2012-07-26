--
select count(*) from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Xs%SegmentCommon%';
--  We should remove these 287490 records
  delete from catalogue_opticalproduct where genericsensorproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Xs%SegmentCommon%');
  delete from catalogue_genericsensorproduct where genericimageryproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Xs%SegmentCommon%');
  delete from catalogue_genericimageryproduct where genericproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Xs%SegmentCommon%');
  delete from catalogue_searchrecord where product_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Xs%SegmentCommon%');
  delete from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Xs%SegmentCommon%';
--
select count(*) from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Pan%SegmentCommon%';
-- We should remove these 287490 records
  delete from catalogue_opticalproduct where genericsensorproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Pan%SegmentCommon%');
  delete from catalogue_genericsensorproduct where genericimageryproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Pan%SegmentCommon%');
  delete from catalogue_genericimageryproduct where genericproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Pan%SegmentCommon%');
  delete from catalogue_searchrecord where product_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Pan%SegmentCommon%');
  delete from catalogue_genericproduct where metadata like '%Sensor: Spot 1,2,3 HRV Pan%SegmentCommon%';

--
-- Sensor: Spot 4 Pan
select count(*) from catalogue_genericproduct where metadata like '%Sensor: Spot 4 Pan%SegmentCommon%';
-- We should remove these 186201 records
  delete from catalogue_opticalproduct where genericsensorproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 4 Pan%SegmentCommon%');
  delete from catalogue_genericsensorproduct where genericimageryproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 4 Pan%SegmentCommon%');
  delete from catalogue_genericimageryproduct where genericproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 4 Pan%SegmentCommon%');
  delete from catalogue_searchrecord where product_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 4 Pan%SegmentCommon%');
  delete from catalogue_genericproduct where metadata like '%Sensor: Spot 4 Pan%SegmentCommon%';

-- Sensor: Spot 4 G,R,NIR,SWIR
select count(*) from catalogue_genericproduct where metadata like '%Sensor: Spot 4 G,R,NIR,SWIR%SegmentCommon%';
--  We should remove these 222263 records
  delete from catalogue_opticalproduct where genericsensorproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 4 G,R,NIR,SWIR%SegmentCommon%');
  delete from catalogue_genericsensorproduct where genericimageryproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 4 G,R,NIR,SWIR%SegmentCommon%');
  delete from catalogue_genericimageryproduct where genericproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 4 G,R,NIR,SWIR%SegmentCommon%');
  delete from catalogue_searchrecord where product_id in (select id from catalogue_genericproduct where metadata like '%Sensor: Spot 4 G,R,NIR,SWIR%SegmentCommon%');
  delete from catalogue_genericproduct where metadata like '%Sensor: Spot 4 G,R,NIR,SWIR%SegmentCommon%';


-- Final test:
 select count(*) from catalogue_genericproduct where metadata like '%Sensor: Spot %' limit 1;
-- count 
-------
--     0
--(1 row)

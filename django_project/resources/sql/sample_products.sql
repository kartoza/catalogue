-- sample 1000 optical products
-- 
-- **************       IMPORTANT      ********************
-- after execution, termporary add 'db_table' to Meta class
-- **************       IMPORTANT      ********************
-- 
-- for each of the five models in catalogue/models/products.py
-- run, for each of five models
-- python manage.py dumpdata --format=json --indent=4 catalogue.genericproduct > catalogue/fixtures/test_genericproduct.json 
-- python manage.py dumpdata --format=json --indent=4 catalogue.genericimageryproduct > catalogue/fixtures/test_genericimageryproduct.json 
-- python manage.py dumpdata --format=json --indent=4 catalogue.genericsensorproduct > catalogue/fixtures/test_genericsensorproduct.json 
-- python manage.py dumpdata --format=json --indent=4 catalogue.opticalproduct > catalogue/fixtures/test_opticalproduct.json 
-- python manage.py dumpdata --format=json --indent=4 catalogue.radarproduct > catalogue/fixtures/test_radarproduct.json
-- manually drop creted tables after data export

drop table sample_opticalproduct;

create table sample_opticalproduct AS 
SELECT * from catalogue_opticalproduct
ORDER BY random()
LIMIT 95;

-- create 50 random radarproducts 
DROP table sample_radarproduct;
create table sample_radarproduct AS 
SELECT * from catalogue_radarproduct
ORDER BY random()
LIMIT 5;

-- for that 100 products create parent tables
drop table sample_genericsensorproduct;
create table sample_genericsensorproduct AS
select b.* from sample_opticalproduct a inner join catalogue_genericsensorproduct b
ON a.genericsensorproduct_ptr_id = b.genericimageryproduct_ptr_id
UNION ALL
select b.* from sample_radarproduct a inner join catalogue_genericsensorproduct b
ON b.genericimageryproduct_ptr_id = a.genericsensorproduct_ptr_id;

drop table sample_genericimageryproduct;
create table sample_genericimageryproduct AS
select b.* from sample_genericsensorproduct a inner join catalogue_genericimageryproduct b
ON  a.genericimageryproduct_ptr_id = b.genericproduct_ptr_id;

drop table sample_genericproduct;
create table sample_genericproduct AS
select b.* from sample_genericimageryproduct a inner join catalogue_genericproduct b
ON  a.genericproduct_ptr_id = b.id;


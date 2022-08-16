I think I've already explained in my previous emails and chat what I think can
be done to automatically reclassify the "bad" products, please read the
following lines and ask me if they are not clear, I attached some code so that
you can understand even better.

Since I dont' know how much garbage is in the OLD DB I cannot tell you if this
approach will work, want to try ?

You can loop through the "bad" products parsing their product_id with something like



from catalogue.models import *

for p in GenericSensorProduct.objects.filter(product_id__startswith='L')[:10]:
    p.productIdReverse(force=True)
    p.save()


this will reclassify the first 10 landsat products creating the missing pieces of the sensor hierarchy.

You can do the same for SPOT:

 
 for i in range(1,6):
     for p in GenericSensorProduct.objects.filter(product_id__startswith="S%s" % i)[:10]:
         p.productIdReverse(force=True)
         p.save()


After doing this, you can check by hand the values in the sensors dictionaries
and fill in the missing "name" or "operator_abbreviation" for the rows that
have been automatically created, not a big work.

Note: this approach will fail if the product_id are not consistent with the
schema in the specs, to enforce this, you can also build a more specific
filter on the product_id, such as 
GenericSensorProduct.objects.filter(product_id__startswith="L%s-_MSS_HRT_MST" % i)

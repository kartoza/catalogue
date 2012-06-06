class CatalogueRouter(object):
    """A router to control all database operations on models in
       the project. Requests for the legacy acscatalogue will be
       routed to sac_old, all other requests to sac. This allows
       the sac db to be very clean without all the old gunk inherited
       from informix.
       see http://docs.djangoproject.com/en/dev/topics/db/multi-db/
       for more info on django db routing. Note this requires Django 1.2
       """

    def db_for_read(self, model, **hints):
        "Point all operations on acscatalogue models to 'acs'"
        if model._meta.app_label == 'acscatalogue':
            return 'acs'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on acscatalogue models to 'acs'"
        if model._meta.app_label == 'acscatalogue':
            return 'acs'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in acscatalogue is not involved"
        if obj1._meta.app_label != 'acscatalogue' or obj2._meta.app_label != 'acscatalogue':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the acscatalogue app only appears on the 'acs' db"
        if db == 'acs':
            return model._meta.app_label == 'acscatalogue'
        elif model._meta.app_label == 'acscatalogue':
            return False
        return None

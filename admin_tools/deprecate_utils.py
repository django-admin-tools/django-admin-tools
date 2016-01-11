"""
This module contains some utils for easy deprecation warnings.
"""
import warnings


def import_path_is_changed(old_name, new_name):
    class ImportDeprecationMixin(object):
        def __new__(cls, *args, **kwargs):
            klass = super(ImportDeprecationMixin, cls).__new__(cls)
            msg = '%s: %s is deprecated. Please use %s instead.' % (
                klass, old_name, new_name
            )
            warnings.warn(msg, DeprecationWarning)
            return klass
    return ImportDeprecationMixin

from django.utils.functional import (
    cached_property as _cached_property,
)

cached_property = _cached_property


class ConstantValueProperty(object):
    def __init__(self, val):
        self.val = val

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return self.val

    def __set__(self, instance, value):
        # ignore
        pass


class AttrTupleProperty(object):
    def __init__(self, *attrs: str):
        self.attrs = attrs

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return tuple(
            getattr(instance, attr)
            for attr in self.attrs
        )

    def __set__(self, instance, value):
        # ignore
        pass

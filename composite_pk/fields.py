from functools import (
    lru_cache as _lru_cache,
)

from django.db.models import (
    Field as _Field,
    AutoField as _AutoField,
)
from django.db.models.query_utils import (
    DeferredAttribute as _DeferredAttribute,
)

from .query_utils import (
    CompositePrimaryKeyDeferredAttribute as _CPKDeferredAttribute,
)

BaseField = _AutoField


class CompositePrimaryKey(BaseField):
    def __init__(
            self,
            *fields: str,
            **options,
    ):
        self.concrete = False
        super().__init__(**options)
        self.primary_key = True
        self.fields = fields

    @classmethod
    @_lru_cache(maxsize=None)
    def get_lookups(cls):
        lookups = super().get_lookups()
        return {
            'exact': lookups['exact'],
        }

    def set_attributes_from_name(self, name):
        super().set_attributes_from_name(name)
        self.concrete = False

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if args:
            raise ValueError('args from super().deconstruct() should be [] - check django compatibility')
        return name, path, self.fields, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        if isinstance(getattr(cls, self.attname), _DeferredAttribute):
            # replace the deferred attribute
            setattr(cls, self.attname, _CPKDeferredAttribute(*self.fields))

    def get_prep_value(self, value):
        return _Field.get_prep_value(self, value)


from .lookups import (
    CompositePrimaryKeyExact as _CPKExact,
)

CompositePrimaryKey.register_lookup(_CPKExact)

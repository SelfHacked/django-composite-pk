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

from .util import (
    ConstantValueProperty as _Constant,
    AttrTupleProperty as _AttrTuple,
)

BaseField = _AutoField


class CompositePrimaryKey(BaseField):
    def __init__(
            self,
            *fields: str,
            **options,
    ):
        super().__init__(**options)
        self.fields = fields

    primary_key = _Constant(True)
    concrete = _Constant(False)

    @classmethod
    @_lru_cache(maxsize=None)
    def get_lookups(cls):
        lookups = super().get_lookups()
        return {
            'exact': lookups['exact'],
        }

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if args:
            raise ValueError('args from super().deconstruct() should be [] - check django compatibility')
        return name, path, self.fields, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        if isinstance(getattr(cls, self.attname), _DeferredAttribute):
            # replace the deferred attribute
            setattr(cls, self.attname, _AttrTuple(*self.fields))

    def get_prep_value(self, value):
        return _Field.get_prep_value(self, value)


from .lookups import (
    CompositePrimaryKeyExact as _CPKExact,
)

CompositePrimaryKey.register_lookup(_CPKExact)

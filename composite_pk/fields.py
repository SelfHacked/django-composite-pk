import logging as _logging
import typing as _typing
from functools import (
    lru_cache as _lru_cache,
)

from django.db.models import (
    Field as _Field,
    AutoField as _AutoField,
)
from django.db.models.options import (
    Options as _Options,
)
from django.db.models.query_utils import (
    DeferredAttribute as _DeferredAttribute,
)
from model_wrappers import (
    FieldWrapper as _FieldWrapper,
    ModelWrapper as _ModelWrapper,
)
from returns import (
    returns as _returns,
)

from .util import (
    cached_property,
    ConstantValueProperty as _Constant,
    AttrTupleProperty as _AttrTuple,
)

BaseField = _AutoField

logger = _logging.getLogger(__name__)


class CompositePrimaryKey(BaseField):
    def __init__(
            self,
            *fields: str,
            **options,
    ):
        super().__init__(**options)
        self.field_names = fields

    primary_key = _Constant(True)
    concrete = _Constant(False)

    @cached_property
    def wrapper(self) -> _FieldWrapper:
        return _FieldWrapper(self)

    @property
    def model_wrapper(self) -> _ModelWrapper:
        return self.wrapper.model

    @cached_property
    @_returns(tuple)
    def fields(self) -> _typing.Sequence[_FieldWrapper]:
        for name in self.field_names:
            yield self.model_wrapper.get_field(name=name)

    def get_col(self, alias, output_field=None):
        if output_field is None:
            output_field = self
        if alias != self.model_wrapper.table_name or output_field != self:
            return _CPKCol(alias, self, output_field)
        else:
            return self.cached_col

    @cached_property
    def cached_col(self):
        return _CPKCol(self.model_wrapper.table_name, self)

    @classmethod
    @_lru_cache(maxsize=None)
    def get_lookups(cls):
        lookups = super().get_lookups()
        return {
            'exact': lookups['exact'],
            'in': lookups['in'],
        }

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if args:
            raise ValueError(
                'args from super().deconstruct() should be [] - '
                'check django compatibility',
            )
        return name, path, self.field_names, kwargs

    def _check_unique_together(self, meta: _Options):
        for uniq in meta.unique_together:
            if set(uniq) == set(self.field_names):
                return
        logger.warning(
            '`unique_together` for composite primary key '
            f'{self.field_names} not set',
        )

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        if isinstance(getattr(cls, self.attname), _DeferredAttribute):
            # replace the deferred attribute
            setattr(cls, self.attname, _AttrTuple(*self.field_names))
        self._check_unique_together(self.model_wrapper.meta)

    def get_prep_value(self, value):
        return _Field.get_prep_value(self, value)


from .expressions import (  # noqa: E402
    CompositePrimaryKeyColumn as _CPKCol,
)

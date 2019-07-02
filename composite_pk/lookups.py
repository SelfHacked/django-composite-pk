from typing import Tuple

from django.db.models.lookups import (
    Exact as _Exact,
)
from model_wrappers import (
    ModelWrapper as _ModelWrapper,
    FieldWrapper as _FieldWrapper,
)

from .util import cached_property


class CompositePrimaryKeyExact(_Exact):
    @property
    def alias(self) -> str:
        return self.lhs.alias

    @property
    def target(self) -> '_CPK':
        return self.lhs.target

    @property
    def fields(self) -> Tuple[str, ...]:
        return self.target.fields

    @cached_property
    def field(self) -> _FieldWrapper:
        return _FieldWrapper(self.target)

    @property
    def model(self) -> _ModelWrapper:
        return self.field.model

    def as_sql(self, compiler, connection):
        if len(self.fields) != len(self.rhs):
            raise ValueError

        sqls = []
        params = []
        for field, rhs in zip(self.fields, self.rhs):
            lhs = self.model.get_field(name=field).col(self.alias)
            sql, param = _Exact(lhs, rhs).as_sql(compiler, connection)
            sqls.append(sql)
            params.extend(param)

        return '((' + ') AND ('.join(sqls) + '))', params


from composite_pk.fields import (
    CompositePrimaryKey as _CPK,
)

from django.db.models.expressions import (
    Col as _Col,
)
from django.db.models.lookups import (
    Exact as _Exact,
)


class CompositePrimaryKeyExact(_Exact):
    @property
    def alias(self) -> str:
        return self.lhs.alias

    @property
    def pk_field(self) -> '_CPK':
        return self.lhs.target

    @property
    def fields(self):
        return self.pk_field.fields

    @property
    def model(self):
        return self.pk_field.model

    def get_field(self, field: str):
        for f in self.model._meta.fields:
            if f.name == field:
                return f
        raise ValueError

    def as_sql(self, compiler, connection):
        if len(self.fields) != len(self.rhs):
            raise ValueError

        sqls = []
        params = []
        for field, rhs in zip(self.fields, self.rhs):
            lhs = _Col(self.alias, self.get_field(field))
            sql, param = _Exact(lhs, rhs).as_sql(compiler, connection)
            sqls.append(sql)
            params.extend(param)

        return '((' + ') AND ('.join(sqls) + '))', params


from composite_pk.fields import (
    CompositePrimaryKey as _CPK,
)

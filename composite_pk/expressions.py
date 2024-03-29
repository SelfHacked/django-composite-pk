from django.db.models.expressions import (
    Col as _Col,
)


class CompositePrimaryKeyColumn(_Col):
    def as_sql(self, compiler, connection):
        sqls = []
        params = []
        target: _CPK = self.target
        for field in target.fields:
            col = field.col(self.alias)
            sql, param = col.as_sql(compiler, connection)
            sqls.append(sql)
            params.extend(param)
        final_sql = '(' + ','.join(sqls) + ')'
        return final_sql, params


from .fields import (  # noqa: E402
    CompositePrimaryKey as _CPK,
)

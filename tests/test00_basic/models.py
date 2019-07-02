from django.db import models

from composite_pk.fields import CompositePrimaryKey


class A(models.Model):
    x = models.IntegerField()
    y = models.CharField(max_length=8)
    primary_key = CompositePrimaryKey('x', 'y')
    text = models.TextField(null=True)

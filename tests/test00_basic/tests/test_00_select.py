import pytest

from ..models import A


@pytest.mark.django_db
def test_get_value():
    assert set(a.primary_key for a in A.objects.all()) == {
        (1, 'a'),
        (2, 'abc'),
    }

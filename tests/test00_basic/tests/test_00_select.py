import pytest

from ..models import A


@pytest.mark.django_db
def test_get_value():
    assert set(a.primary_key for a in A.objects.all()) == {
        (1, 'a'),
        (2, 'abc'),
    }


@pytest.mark.django_db
def test_exact_lookup():
    a = A.objects.get(primary_key=(1, 'a'))
    assert a.x == 1
    assert a.y == 'a'
    assert a.text == 'sample text'
    assert a.primary_key == (1, 'a')

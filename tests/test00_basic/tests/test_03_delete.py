import pytest

from ..models import A


@pytest.mark.xfail(reason='`in` lookup not supported')
@pytest.mark.django_db
def test_obj_delete():
    a = A.objects.get(x=2)
    a.delete()

    assert {a.primary_key for a in A.objects.all()} == {
        (1, 'a'),
        (1, 'b'),
    }


@pytest.mark.django_db
def test_manager_delete_pk():
    A.objects.filter(primary_key=(1, 'b')).delete()

    assert {a.primary_key for a in A.objects.all()} == {
        (1, 'a'),
        (2, 'abc'),
    }


@pytest.mark.django_db
def test_manager_delete_all():
    A.objects.all().delete()

    assert not A.objects.exists()


@pytest.mark.django_db
def test_manager_delete_filter():
    A.objects.filter(x=1).delete()

    assert {a.primary_key for a in A.objects.all()} == {
        (2, 'abc'),
    }

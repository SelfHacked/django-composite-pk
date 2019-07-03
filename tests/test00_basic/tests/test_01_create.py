import pytest

from ..models import A


@pytest.mark.django_db
def test_manager_create():
    a = A.objects.create(
        x=3,
        y='yyy',
        text='testtest',
    )
    assert a.primary_key == (3, 'yyy')

    assert A.objects.get(x=3).primary_key == (3, 'yyy')


@pytest.mark.django_db
def test_obj_create():
    a = A(
        x=3,
        y='yyy',
        text='testtest',
    )
    assert a.primary_key == (3, 'yyy')

    a.save()
    assert a.primary_key == (3, 'yyy')

    assert A.objects.get(x=3).primary_key == (3, 'yyy')

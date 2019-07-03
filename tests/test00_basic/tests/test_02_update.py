import pytest

from ..models import A


@pytest.mark.django_db
def test_obj_update():
    a = A.objects.get(x=2)
    a.text = 'testtesttest'
    a.save()

    assert A.objects.get(x=2).text == 'testtesttest'


@pytest.mark.django_db
def test_manager_update_pk():
    A.objects.filter(primary_key=(1, 'a')).update(text='tttttt')
    assert A.objects.get(x=1).text == 'tttttt'
    assert A.objects.get(x=2).text is None


@pytest.mark.django_db
def test_manager_update_all():
    A.objects.all().update(text='tttttt')
    assert A.objects.get(x=1).text == 'tttttt'
    assert A.objects.get(x=2).text == 'tttttt'


@pytest.mark.django_db
def test_manager_update_filter():
    A.objects.filter(x__in=(1, 2)).update(text='tttttt')
    assert A.objects.get(x=1).text == 'tttttt'
    assert A.objects.get(x=2).text == 'tttttt'

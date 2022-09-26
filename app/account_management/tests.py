# from django.test import TestCase

# Create your tests here.
import pytest
from .models import *


@pytest.mark.django_db
def test_initialize_objects_in_database():
    asset = AccountType.objects.create(name="AS")

    current_asset = AccountCategory.objects.create(name="Current Asset", taip=asset)

    cash_account = Account(name="Cash", category=current_asset)

    cash_account.save()

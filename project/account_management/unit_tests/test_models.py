# from django.test import TestCase

# Create your tests here.
import pytest
from account_management.models import *


@pytest.mark.django_db
def test_initialize_objects_in_database():
    current_asset = AccountCategory.objects.create(name="Current Asset", group="AS", )
    cash_account = Account(number=1, category=current_asset)

    cash_account.save()

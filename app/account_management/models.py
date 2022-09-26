from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Account(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    debit_balance = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    category = models.ForeignKey(
        "AccountCategory", on_delete=models.CASCADE, related_name="accounts"
    )


class AccountCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    taip = models.ForeignKey(
        "AccountType",
        on_delete=models.CASCADE,
        related_name="categories",
    )


class AccountType(models.Model):
    name = models.CharField(
        max_length=2,
        choices=[
            ("AS", _("Assets")),
            ("LI", _("Liabilities")),
            ("CA", _("Capital")),
            ("RV", _("Revenue")),
            ("EX", _("Expense")),
        ],
    )

    def get_all_accounts(self):
        return Account.objects.filter(category__taip=self)

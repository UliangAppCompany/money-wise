from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Account(models.Model):
    number = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    should_debit_balance = models.BooleanField(default=True)
    credit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    category = models.ForeignKey(
        "AccountCategory", on_delete=models.CASCADE, related_name="accounts"
    )

    def __repr__(self) -> str:
        return f'<{self.number}-{self.description}>'
        
    @property
    def balance(self):
        return (
            self.debit_balance - self.credit_balance
            if self.should_debit_balance
            else self.credit_balance - self.debit_balance
        )


class AccountCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    supercategory = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="subcategories", null=True
    )

    def __repr__(self): 
        return f'<{self.name}>' 

    def get_all_category_accounts(self):
        stack = [self] 
        resultset = []
        while stack: 
            cat = stack.pop() 
            qs = Account.objects.filter(category=cat)
            if qs.count():
                resultset.extend([account for account in qs.all()])
            else: 
                stack.extend([subcat for subcat in cat.subcategories.all()])
        return resultset
    
    def get_category_subtotals(self): 
        return sum(account.balance for account in self.get_all_category_accounts()) 
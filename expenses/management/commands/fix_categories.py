from django.core.management.base import BaseCommand
from expenses.models import Transaction, Category

class Command(BaseCommand):
    help = 'Fix invalid category references in Transaction table'

    def handle(self, *args, **kwargs):
        # Step 1: Fetch all valid categories
        category_map = dict(Category.objects.values_list('name', 'id'))
        self.stdout.write(f"Valid categories: {category_map}")

        # Step 2: Fix transactions with invalid category names
        transactions_fixed = 0
        invalid_transactions = Transaction.objects.filter(category__in=category_map.keys())
        for transaction in invalid_transactions:
            if transaction.category in category_map:
                transaction.category_id = category_map[transaction.category]
                transaction.save()
                transactions_fixed += 1

        self.stdout.write(f"Fixed {transactions_fixed} transactions.")

        # Step 3: Check for remaining invalid categories
        remaining_invalid = (
            Transaction.objects.exclude(category__in=Category.objects.values_list('id', flat=True))
        )
        if remaining_invalid.exists():
            self.stdout.write(
                f"Remaining invalid transactions: {remaining_invalid.count()}. Manual intervention required."
            )
        else:
            self.stdout.write("All transactions are now valid.")

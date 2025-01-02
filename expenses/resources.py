from import_export import resources, fields
from expenses.models import Transaction, Category
from datetime import datetime

class TransactionResource(resources.ModelResource):
    date = fields.Field(
        column_name='Data',  # Italian header for the date field
        attribute='date',
    )
    description = fields.Field(
        column_name='Operazione',  # Italian header for the description
        attribute='description',
    )
    category = fields.Field(
        column_name='Categoria',  # Italian header for the category
        attribute='category',
    )
    amount = fields.Field(
        column_name='Importo',  # Italian header for the amount
        attribute='amount',
    )
    type = fields.Field(
        column_name='Importo',  # Same column used to determine the type
        attribute='type',
    )

    def before_import_row(self, row, **kwargs):
    # Validate 'Valuta'
        if row.get('Valuta', 'EUR').strip().upper() != 'EUR':
            raise ValueError(f"Non-EUR currency found: {row.get('Valuta')}")

        # Process 'date'
        if 'Data' in row:
            row['date'] = self.parse_date(row['Data'])

        # Process 'category'
        category_name = row.get('Categoria', '').strip()
        if not category_name:
            raise ValueError(f"Missing category in row: {row}")

        # Attempt to get or create the category
        try:
            category = self.get_or_create_category(category_name)
            if category:
                row['category'] = category.id
            else:
                raise ValueError(f"Unable to process category: {category_name}")
        except Exception as e:
            raise ValueError(f"Error handling category '{category_name}': {e}")
        
        # Process 'amount' and 'type'
        if 'Importo' in row:
            row['amount'], row['type'] = self.parse_amount_and_type(row['Importo'])

    def parse_date(self, raw_date):
        try:
            # Attempt parsing in DD/MM/YYYY format
            return datetime.strptime(raw_date, "%d/%m/%Y").date()
        except ValueError:
            try:
                # Attempt parsing in YYYY-MM-DD format
                return datetime.strptime(raw_date, "%Y-%m-%d").date()
            except ValueError:
                # Raise an error if none of the formats match
                raise ValueError(f"Invalid date format: {raw_date}. Expected formats: DD/MM/YYYY or YYYY-MM-DD.")

    def get_or_create_category(self, category_name):
        """
        Get an existing category or create a new one if it doesn't exist.
        """
        try:
            # Normalize category name (e.g., capitalize, remove extra spaces)
            normalized_name = category_name.title()

            # Get or create the category
            category, created = Category.objects.get_or_create(name=normalized_name)

            # Optional logging or debugging
            if created:
                print(f"Created new category: {normalized_name}")

            return category
        except Exception as e:
            print(f"Error creating category: {category_name} - {e}")
            return None

    def parse_amount_and_type(self, raw_amount):
        try:
            # Convert amount and determine type
            amount = float(raw_amount.replace(',', '.'))  # Replace commas with dots
            transaction_type = 'expense' if amount < 0 else 'income'
            return abs(amount), transaction_type
        except ValueError:
            raise ValueError(f"Invalid amount: {raw_amount}. Must be a valid number.")

    class Meta:
        model = Transaction
        fields = ('amount', 'type', 'date', 'category', 'description')

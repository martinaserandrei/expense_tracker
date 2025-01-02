import pytest
from expenses.factories import TransactionFactory

@pytest.fixture
def transactions():
    return TransactionFactory.create_batch(20)
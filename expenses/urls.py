from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, transactions_list, new_transaction, feedback_view, update_transaction,delete_transaction,transaction_add_success,get_transactions,transaction_charts,export,import_transactions

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(template_name='expenses/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('transactions/', transactions_list, name='transactions'),
    path('new_transaction/', new_transaction, name='new_transaction'),
    path('feedback/', feedback_view, name='feedback'),
    path('charts/', transaction_charts, name='charts'),
    path('transactions/<int:pk>/update/',update_transaction, name='update_transaction'),
    path('transactions/<int:pk>/delete/',delete_transaction, name='delete_transaction'),
    path('success',transaction_add_success,name='transaction_add'),
    path('get_transactions/',get_transactions, name='get_transactions'),
    path('transactions/export',export,name='export'),
    path('transactions/import',import_transactions,name='import'),
]

from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm,CustomUserCreationForm, FeedbackForm
from django.http import JsonResponse
from django_filters.views import FilterView
from expenses.filters import TransactionFilter
from django.contrib import messages
from django.http import HttpResponse
import expenses.charting as ch 
from django_htmx.http import retarget
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
import time
from expenses.resources import TransactionResource
from tablib import Dataset
from django.views.decorators.http import require_http_methods



def welcome(request):
    return render(request, 'expenses/welcome.html')

def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        if request.headers.get('HX-Request'):  # HTMX request
            return JsonResponse({'message': 'Account created successfully!'})
        return redirect('login')  # Redirect to login page

    if request.htmx:  # HTMX request
        return render(request, 'expenses/partials/signup_form.html', {'form': form})
    
    return render(request, 'expenses/signup.html', {'form': form})


@login_required
def home(request):
    """Display the expense page."""
    return render(request, "expenses/home.html")

def new_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            # Render a success partial if HTMX is used
            if request.htmx:
                context = {'transaction': transaction}
                response = render(request, 'expenses/partials/transaction_add_success.html', context)
                return retarget(response, '#transaction-block')  # Update only the specified block

            # Redirect for non-HTMX requests
            return redirect('transactions')
        else:
            # Return form errors for HTMX
            if request.htmx:
                response = render(request, 'expenses/partials/new_transaction_p.html', {'form': form})
                return retarget(response, '#transaction-block')

            # Render the full page for non-HTMX requests
            return render(request, 'expenses/new_transaction.html', {'form': form})

    # GET request: Render the form
    form = TransactionForm()
    if request.htmx:
        return render(request, 'expenses/partials/new_transaction_p.html', {'form': form})
    return render(request, 'expenses/new_transaction.html', {'form': form})

def transactions_list(request):
    transaction_filter = TransactionFilter(request.GET, queryset=Transaction.objects.filter(user=request.user).order_by('-date'))
    transactions = transaction_filter.qs
    paginator=Paginator(transactions,settings.PAGE_SIZE)
    transaction_page = paginator.page(1)

    # Use methods from TransactionQuerySet
    total_income = transactions.get_total_income()
    total_expenses = transactions.get_total_expenses()

    context = {
        'transactions': transaction_page,
        'filter': transaction_filter,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': total_income-total_expenses,
    }
    if request.htmx:  # HTMX request
        return render(request, 'expenses/partials/transaction_container.html', context)
    return render(request, 'expenses/transaction_list.html', context)

#primary key to retrieve the transaction to modify
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user= request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST,instance=transaction)
        if form.is_valid():
            transaction = form.save()
            context= {'transaction': transaction,}
            return render( request, 'expenses/partials/transaction_success.html', context)
        else:
            context={'form': form, 'transaction':transaction,}
            response= render(request, 'expenses/partials/update_transaction.html',context)
            return retarget(response,'#transaction-block')
    context={'form': TransactionForm(instance=transaction), 'transaction':transaction,}
    return render(request, 'expenses/partials/update_transaction.html',context)

def transaction_add_success(request):
    context = {
        'message': "Transaction has been successfully added to the list!"
    }
    return render(request, 'expenses/partials/transaction_add_success.html', context)

@require_http_methods(["DELETE"])
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user= request.user)
    transaction.delete()
    context= {
        'message': f"Transaction of {transaction.amount} on {transaction.date} was deleted succesfully!"
    }
    return render(request, 'expenses/partials/transaction_delete_success.html',context)


def get_transactions(request):
    time.sleep(2)
    page = request.GET.get('page',1)
    transaction_filter = TransactionFilter(request.GET, queryset=Transaction.objects.filter(user=request.user).order_by('-date'))
    transactions = transaction_filter.qs
    paginator=Paginator(transactions,settings.PAGE_SIZE)
    context={
        'transactions': paginator.page(page)
    }
    return render( request, 'expenses/partials/transaction_container.html#transaction_list',context)

def feedback_view(request):
    if request.method == 'POST':
        # Handle feedback submission
        bio = request.POST.get('bio')
        # Save the feedback (replace with your actual save logic)
        if bio:
            # Simulate saving feedback
            messages.success(request, "Thank you for your feedback!")
            if request.headers.get('HX-Request'):
                # Return a success message for HTMX
                return HttpResponse("<p class='text-success'>Thank you for your feedback!</p>")
    
    if request.headers.get('HX-Request'):
        # If the request is an HTMX request, return only the form partial
        return render(request, 'expenses/_feedback_form.html')
    
    # Otherwise, render the full feedback page
    return render(request, 'expenses/feedback.html')

def transaction_charts(request):
    # Debugging: Ensure the user is passed correctly
    print("User:", request.user)

    # Apply the filter to user's transactions
    transaction_filter = TransactionFilter(
        request.GET, 
        queryset=Transaction.objects.filter(user=request.user))

    # Generate the chart using the filtered transactions
    income_expense_bar = ch.plot_expenses(transaction_filter.qs)
    category_income_pie = ch.plot_category_pie_chart(
        transaction_filter.qs.filter(type='income'))
    category_expense_pie = ch.plot_category_pie_chart(
        transaction_filter.qs.filter(type='expense'))
    plot_line_chart = ch.plot_line_chart(transaction_filter.qs)

    context = {
        'filter': transaction_filter,
        'income_expense_bar': income_expense_bar.to_html(),
        'category_income_pie': category_income_pie.to_html(),
        'category_expense_pie': category_expense_pie.to_html(),
        'plot_line_chart': plot_line_chart.to_html(),
    }
    if request.htmx:
        return render(request, 'expenses/partials/charts_container.html', context)
    return render(request, 'expenses/charts.html', context)

def export(request):
    if request.htmx:
        return HttpResponse(headers={'HX-Redirect':request.get_full_path()})
    transaction_filter = TransactionFilter(request.GET, queryset=Transaction.objects.filter(user=request.user).order_by('-date'))
    data= TransactionResource().export(transaction_filter.qs)
    response= HttpResponse(data.csv)
    #pip install "tablib[all]" to install also pandas file yaml files and all files
    response['Content-Disposition']='attachment;filename=transactions.csv'
    return response


def import_transactions(request):
    if request.method == 'POST':
        dataset = Dataset()
        file = request.FILES['file']

        dataset.load(file.read().decode('utf-8'), format='csv')
        resource = TransactionResource()
        result = resource.import_data(dataset, dry_run=True)

        # Collect errors
        error_messages = []
        for row_number, row_errors in result.row_errors():
            for error in row_errors:
                error_messages.append(str(error))

        if not error_messages:
            resource.import_data(dataset, dry_run=False)
            return render(request, 'expenses/partials/transaction_success.html', {
                'message': 'Transactions imported successfully!',
            })

        return render(request, 'expenses/partials/transaction_uploaded_success.html', {
            'message': 'Errors occurred during the import process.',
            'errors': error_messages,
        })

    return render(request, 'expenses/partials/import_transaction.html')



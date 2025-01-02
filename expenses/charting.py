import plotly.express as px
from django.db.models import Sum, Q
from expenses.models import Category
import plotly.graph_objects as go


def plot_expenses(qs):
    # Define categories for the chart
    categories = ['Income', 'Expenditure']

    # Calculate total income and total expenditure
    total_income = qs.filter(type='income').aggregate(total=Sum('amount'))['total'] 
    total_expense = qs.filter(type='expense').aggregate(total=Sum('amount'))['total']

    # Create a bar chart using Plotly
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=[total_income, total_expense],
            marker_color=['#2664eb', '#F44336'],  # blue for income, Red for expense
            text=[f'€{total_income:,.2f}', f'€{total_expense:,.2f}'],
            textposition='auto',
            hovertemplate='%{y}',
            showlegend=False
        )
    ])

    # Customize layout for better visuals
    fig.update_layout(
        yaxis_title='Amount (€)',
        template='plotly_white',
        margin=dict(l=40, r=40, t=60, b=60),
    )

    return fig

def plot_category_pie_chart(qs):
    count_per_category = (
        qs.order_by('category').values('category')
        .annotate(total=Sum('amount'))
    )
    category_pks = count_per_category.values_list('category', flat=True).order_by('category')
    categories = Category.objects.filter(pk__in=category_pks).order_by('pk').values_list('name', flat=True)
    total_amounts = count_per_category.values_list('total', flat=True)
    fig = px.pie(names=categories, values=total_amounts)
    return fig

def plot_line_chart(qs):
    # Group the data by month (or day, week, etc.)
    data = qs.values('date__month').annotate(
        total_income=Sum('amount', filter=Q(type='income')),
        total_expense=Sum('amount', filter=Q(type='expense'))).order_by('date__month')

    months = [f'Month {entry["date__month"]}' for entry in data]
    income = [entry['total_income'] or 0 for entry in data]
    expenses = [entry['total_expense'] or 0 for entry in data]

    # Create the line chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=months,
        y=income,
        mode='lines+markers',
        name='Income',
        line=dict(color='#2664eb'),
        hovertemplate='Income: €%{y}'
    ))

    fig.add_trace(go.Scatter(
        x=months,
        y=expenses,
        mode='lines+markers',
        name='Expense',
        line=dict(color='#F44336'),
        hovertemplate='Expense: €%{y}'
    ))

    # Customize layout for better visuals
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Amount (€)',
        template='plotly_white',
        margin=dict(l=40, r=40, t=60, b=60),
    )

    return fig

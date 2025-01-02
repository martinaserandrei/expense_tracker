from django.contrib import admin
from expenses.models import Category,Transaction, Feedback
# Register your models here.
admin.site.register(Transaction)
admin.site.register(Category)
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'submitted_at']
    search_fields = ['user__username', 'bio']
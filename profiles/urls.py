from django.urls import path as url
from . import views

app_name = "profiles"

urlpatterns = [
    url("account_status/", views.index, name = "account_status"),
    url("money_transfer/", views.money_transfer, name = "money_transfer"),
    url("loan_app/", views.loan, name = "loan_app"),
    url("ewallet/", views.ewallet, name = "ewallet"),
    url("online_pay/", views.online_pay, name = "online_pay"),
    url("settings/", views.settings, name = "settings"),
    url("edit_details/", views.edit_details, name = "edit_details"),
    url("delete_account/", views.delete_account, name = "delete_account"),
    url("debit_cards/", views.debit_cards, name = "debit_cards"),
    url("credit_cards/", views.credit_cards, name = "credit_cards"),
    url("statement/", views.statement, name = "statement"),
    url("investment/", views.investment, name = "investment"),
]
"""
app.views
~~~~~~~~~

This module implements the app views.

:copyright: (c) 2019 by Elliott Maguire
"""

from api import utils
from api.models import Account, Contact

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives


def index(request):
    """ Home page. (/) """
    return render(request, 'index.html')


@login_required
def accounts(request):
    """ Accounts page. (accounts/) """
    accounts = Account.objects.all()

    context = {'accounts': accounts}
    return render(request, 'accounts.html', context)


@login_required
def account(request, sfid):
    """ Account page. (accounts/<str:sfid>) """
    account = Account.objects.get(sfid=sfid)
    contacts = Contact.objects.filter(account=account)
    contacts = sorted(contacts,
        key=lambda contact: contact.rating + contact.priority)

    context = {'account': account, 'contacts': contacts}
    return render(request, 'account.html', context)


@login_required
def edit(request, sfid):
    """ Account edit page. (accounts/<str:sfid>/edit) """
    account = Account.objects.get(sfid=sfid)
    contacts = Contact.objects.filter(account=account)
    contacts = sorted(contacts,
        key=lambda contact: contact.rating + contact.priority)

    context = {'account': account, 'contacts': contacts}
    return render(request, 'edit.html', context)


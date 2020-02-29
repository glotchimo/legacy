"""
api.views
~~~~~~~~~

This module implements the API endpoints.

:copyright: (c) 2019 by Elliott Maguire
"""

from api import utils
from api.models import Account, Contact

from django.shortcuts import HttpResponse, redirect
from django.contrib.auth.decorators import login_required


@login_required
def edit_account(request, sfid):
    """ Updates the values on an account. """
    if request.method != 'POST':
        return HttpResponse(content='Invalid request.', status=405)
    else:
        post = request.POST.get

    account = Account.objects.get(sfid=sfid)
    utils.update_object(account, post)

    return redirect('app:edit', sfid=account.sfid)

@login_required
def mark_account(request, sfid, status):
    """ Marks an account for review. """
    account = Account.objects.get(sfid=sfid)

    account.status = status
    account.save()

    return redirect('app:account', sfid=account.sfid)


@login_required
def add_contact(request, sfid):
    """ Adds and queues a new contact. """
    account = Account.objects.get(sfid=sfid)
    contact = Contact.objects.create(account=account, status='review')

    return redirect('app:edit', sfid=contact.account.sfid)


@login_required
def edit_contact(request, cid):
    """ Updates the values on a contact. """
    if request.method != 'POST':
        return HttpResponse(content='Invalid request.', status=405)
    else:
        post = request.POST.get

    contact = Contact.objects.get(id=cid)
    utils.update_object(contact, post)

    return redirect('app:edit', sfid=contact.account.sfid)


@login_required
def queue_contact(request, cid):
    """ Queues a contact to be added to the account. """
    contact = Contact.objects.get(id=cid)

    contact.status = 'upload'
    contact.save()

    return redirect('app:edit', sfid=contact.account.sfid)


@login_required
def queue_contacts(requests, sfid):
    """ Queues all contacts. """
    account = Account.objects.get(sfid=sfid)
    contacts = Contact.objects.filter(account=account)

    for contact in contacts:
        contact.status = 'upload'
        contact.save()

    return redirect('app:edit', sfid=account.sfid)


@login_required
def delete_contact(request, cid):
    """ Deletes a contact. """
    contact = Contact.objects.get(id=cid)
    account = contact.account

    contact.delete()

    return redirect('app:edit', sfid=contact.account.sfid)


"""
app.views
~~~~~~~~~

This module implements the app views for Pathfindr.

:copyright: (c) 2018 by Elliott Maguire
"""

from app.models import Account, Contact

from django.shortcuts import render, redirect


def index(request):
    """ Index view. (/) """
    return render(request, 'index.html')


def tasks(request):
    """ Tasks view. (/tasks) """
    tasks = Account.objects.filter(status='enrich')
    return render(request, 'tasks.html', {
        'tasks': tasks})
    

def enrich(request, sfid):
    """ Enrich view. (/enrich) """
    account = Account.objects.get(sfid=sfid)
    contacts = Contact.objects.filter(account=account, status='enrich')
    contacts = sorted(contacts, key=lambda contact: contact.rating)

    if request.method == 'POST':
        ids = request.POST.getlist('contacts')
        contacts = Contact.objects.filter(account=account, pk__in=ids)
        for contact in contacts:
            contact.status = 'queued'
            contact.save()
        
        account.status = 'queued'
        account.save()

        return redirect('tasks',
            permanent=True,
            sfid=account.sfid)
    
    return render(request, 'enrich.html', {
        'account': account,
        'contacts': contacts})


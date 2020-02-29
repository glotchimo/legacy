"""
app.views
~~~~~~~~~

This module implements the app views.

:copyright: (c) 2019 by Elliott Maguire
"""

from api import utils
from api.models import Account, Contact
from app.models import Profile

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def index(request):
    """ Home page. (/) """
    return render(request, 'index.html')


def signup(request, error=None):
    """ New user sign-up. (signup) """

    # Handle POST submission.
    if request.method == 'POST':
        # Restate POST data.
        post = request.POST.get

        # Confirm password
        if post('password') != post('confirmation'):
            context = {'error': True}
            return render(request, 'registration/signup.html', context)

        # Build and save new user.
        user = User.objects.create_user(
            post('username'),
            email=post('email'),
            password=post('password'),
            first_name=post('first'),
            last_name=post('last'))

        # Create profile for new user.
        Profile.objects.create(user=user, sfid=post('sfid'))

        # Authenticate and log user in.
        user = authenticate(username=post('username'),
                            password=post('password'))
        login(request, user)

        return redirect('app:accounts')

    return render(request, 'registration/signup.html')


@login_required
def accounts(request):
    """ Accounts page. (accounts/) """
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None

    if profile and profile.sfid:
        accounts = Account.objects.filter(prep=str(profile.sfid))
    elif request.user.is_staff:
        accounts = Account.objects.all()
    else:
        accounts = []

    context = {'accounts': accounts}
    return render(request, 'accounts.html', context)


@login_required
def account(request, sfid):
    """ Account page. (accounts/<str:sfid>) """
    account = Account.objects.get(sfid=sfid)
    contacts = Contact.objects.filter(account=account)
    contacts = sorted(
        contacts,
        key=lambda contact: contact.rating + contact.priority)

    old = Contact.objects.filter(account=account, ctype='old').count()
    new = Contact.objects.filter(account=account, ctype='new').count()

    context = {
        'account': account,
        'contacts': contacts,
        'old': old,
        'new': new}
    return render(request, 'account.html', context)


@login_required
def edit(request, sfid):
    """ Account edit page. (accounts/<str:sfid>/edit) """
    account = Account.objects.get(sfid=sfid)
    contacts = Contact.objects.filter(account=account)
    contacts = sorted(contacts,
                      key=lambda contact: contact.rating + contact.priority)

    old = Contact.objects.filter(account=account, ctype='old').count()
    new = Contact.objects.filter(account=account, ctype='new').count()

    context = {
        'account': account,
        'contacts': contacts,
        'old': old,
        'new': new}
    return render(request, 'edit.html', context)

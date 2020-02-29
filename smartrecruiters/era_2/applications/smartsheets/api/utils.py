"""
api.utils
~~~~~~~~~

This module implements utility methods.
"""

import os
import json

from django.contrib.staticfiles.templatetags.staticfiles import static

from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
from gspread import Client
from gspread.exceptions import APIError


def get_session(url, worksheet):
    """ Gets an authenticated session and sheet.

    :param url: a sheet URL
    :param worksheet: a worksheet name
    """
    scopes = [
        'https://www.googleapis.com/auth/drive',
        'https://spreadsheets.google.com/feeds']
    g_credentials = Credentials.from_service_account_file(
        'svc.json',
        scopes=scopes)
    g = Client(auth=g_credentials)
    g.session = AuthorizedSession(g_credentials)

    try:
        sheet = g.open_by_url(url)
        worksheet = sheet.worksheet(worksheet)
    except APIError:
        raise Exception('Failed to fetch sheet.')

    return sheet, worksheet


def get_status(worksheet):
    """ Gets the status (size, progress) of a sheet.

    :param worksheet: a worksheet object
    """
    size = len(worksheet.get_all_records(head=1))
    progress = len(worksheet.findall('Completed'))/size * 100

    return size, int(progress)


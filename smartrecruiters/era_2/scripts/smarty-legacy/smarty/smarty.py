#!/usr/bin/env python

import os
import sys
import time
import json

from smartlib.api import SmartLibrary
from smartlib.exceptions import SmartRecruitersError
from util import Utility

from colorama import init
init()
from colorama import Fore, Back, Style

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

BASE_URL = 'https://api.smartrecruiters.com'


def main():
    clear()
    print(Fore.GREEN + 'Welcome to smarty.py v2.0' + Fore.RESET)
    token = raw_input('If you have a token saved, press enter to choose. Otherwise, please enter your SmartToken to begin:\n')
    global api

    if token:
        try:
            instance = Utility()._get_instance(token)
        except: # Authentication Error
            print(Fore.RED + 'Error 01 - Invalid SmartToken; please try again.' + Fore.RESET)
            time.sleep(2)
            main()
        else: # store new token
            api = SmartLibrary(instance)
            instance['token'] = token
            Utility()._save_token(instance['token'], instance['name'])
            menu(instance)
    else:
        tokenlist = Utility()._list_tokens()
        print(Fore.CYAN + 'Select a token from the following:' + Fore.RESET)
        for i, pair in enumerate(tokenlist):
            print(Fore.LIGHTYELLOW_EX + """
            %s. %s | %s
            """ % (i + 1, pair[0], pair[1])
            + Fore.RESET)

        selection = raw_input('Selection: ')

        try:
            instance = Utility()._get_instance(tokenlist[int(selection) - 1][1])
        except: # Authentication Error
            print(Fore.RED + 'Error 01 - Invalid SmartToken; please try again.' + Fore.RESET)
            time.sleep(2)
            main()
        else:
            api = SmartLibrary(instance)
            instance['token'] = tokenlist[int(selection) - 1][1]
            menu(instance)


def menu(instance):
    """ CLI: Main Menu

    Direct user to other CLI methods.

    Arguments:
        instance -- a dictionary of SR instance properties.
    
    """
    clear()
    print(Fore.GREEN 
          + 'Current Instance: %s (%s)' % (instance['name'], instance['type']) 
          + Fore.RESET)
    print(Fore.CYAN + 'Main Menu - Select an Action' + Fore.RESET)
    print(Fore.LIGHTYELLOW_EX + """
        1. Manage Departments
        2. Manage Jobs
        3. Manage Candidates
        4. Exit
    """  + Fore.RESET)
    selection = raw_input('Selection: ')

    if selection == '':
        print('Invalid input. Please try again.')
        time.sleep(1)
        menu(instance)
    elif selection == '1':
        manage_depts(instance)
    elif selection == '2':
        manage_jobs(instance)
    elif selection == '3':
        manage_candidates(instance)
    elif selection == '4':
        clear()
        print(Fore.GREEN + 'Thanks for using Smarty Py!' + Fore.RESET)
        print(Fore.LIGHTBLACK_EX + """finished with exit code 0""" + Fore.RESET)
        sys.exit()
    else:
        print('Invalid input. Please try again.')
        time.sleep(1)
        menu(instance)


def manage_depts(instance):
    """ CLI: Departments Menu

    List options regarding depts management,
    each tied to one or more smartlib functions.

    Arguments:
        instance -- a dictionary of SR instance information
    
    """
    clear()
    print(Fore.GREEN + 'Current Instance: %s' % (instance['name']) + Fore.RESET)
    print(Fore.CYAN + 'Departments Menu - Select an Action' + Fore.RESET)
    print(Fore.LIGHTYELLOW_EX + """
        1. List Current Departments
        2. List Department Info
        3. Add a Department
        4. Return to Main Menu
    """  + Fore.RESET)

    selection = raw_input('Selection: ')
    if selection == '':
        print('Invalid input. Please try again.')
        time.sleep(1)
        manage_depts(instance)

    elif selection == '1': # list depts
        clear()
        print(Fore.GREEN + 'Current Instance: %s' % (instance['name']) + Fore.RESET)
        print(Fore.CYAN + 'Current Departments:' + Fore.RESET)

        try:
            depts = api.ConfigurationAPI.get_depts()
        except SmartRecruitersError:
            print(Fore.RED + """
            There are currently no existing departments.
            """ + Fore.RESET)
        else:
            if depts:
                for dept in depts:
                    print(Fore.MAGENTA + """
                    %s. %s
                    """ % ((depts.index(dept) + 1), dept)
                    + Fore.RESET)
            else:
                print(Fore.RED + """
                There are currently no existing departments.
                """ + Fore.RESET)

        action = raw_input('Press enter to return to Department Management.')
        if action == '':
            manage_depts(instance)

    elif selection == '2': # list dept info
        clear()
        print(Fore.GREEN + 'Current Instance: %s' % (instance['name']) + Fore.RESET)
        print(Fore.CYAN + 'Department Info' + Fore.RESET)

        dept_id = raw_input('Enter a Department Identifier: ')
        try:
            dept = api.ConfigurationAPI.get_dept(dept_id)
        except SmartRecruitersError:
            print(Fore.RED + """
            There is no department matching that identifier.
            """ + Fore.RESET)
        else:
            if dept:
                print(Fore.CYAN + 'Department Info:' + Fore.RESET)
                for k, v in dept.iteritems():
                    print(Fore.MAGENTA + """
                    %s: %s
                    """ % (k, v)
                    + Fore.RESET)
            else:
                print(Fore.RED + """
                There is no department matching that identifier.
                """ + Fore.RESET)

        action = raw_input('Press enter to return to Department Management.')
        if action == '':
            manage_depts(instance)

    elif selection == '3': # add dept
        clear()
        print(Fore.GREEN + 'Current Instance: %s' % (instance['name']) + Fore.RESET)
        
        label = raw_input('Enter the name of the department to add: ')
        description = raw_input('Enter a short description of the department: ')
        try:
            api.ConfigurationAPI.create_dept(label, description)
        except SmartRecruitersError:
            print(Fore.RED + """
            There was an error creating that department.
            Please make sure that department does not already exist.
            """ + Fore.RESET)
        else:
            print(Fore.LIGHTGREEN_EX + 'Department created.' + Fore.RESET)
            time.sleep(1)
            manage_depts(instance)

    elif selection == '4':
        menu(instance)

    else:
        print('Invalid input. Please try again.')
        time.sleep(1)
        manage_depts(instance)

    time.sleep(2)
    menu(instance)


def manage_jobs(instance):
    clear()
    print('jobs menu')
    time.sleep(2)
    menu(instance)


def manage_candidates(instance):
    """ CLI: Candidates Menu

    List options regarding candidate management,
    each tied to one or more smartlib functions.

    Arguments:
        instance -- a dictionary of SR instance information
    
    """
    clear()
    print(Fore.GREEN + 'Current Instance: %s' % (instance['name']) + Fore.RESET)
    print(Fore.CYAN + 'Departments Menu - Select an Action' + Fore.RESET)
    print(Fore.LIGHTYELLOW_EX + """
        1. Search Candidates
        2. Add Candidate
        3. Add Candidate and Assign to Job
        4. Get Candidate Info
        5. Return to Main Menu
    """  + Fore.RESET)

    selection = raw_input('Selection: ')
    if selection == '':
        print('Invalid input. Please try again.')
        time.sleep(1)
        manage_depts(instance)

    elif selection == '1': # search candidates
        clear()
        print(Fore.GREEN + 'Current Instance: %s' % (instance['name']) + Fore.RESET)
        print(Fore.CYAN + 'Candidate Search' + Fore.RESET)

        q = raw_input('Search Term: ')
        l = raw_input('Limit: ')
        o = raw_input('Offset: ')
        try:
            results = api.CandidateAPI.search(
                {
                    'q': q,
                    'limit': l,
                    'offset': o
                }
            )
        except SmartRecruitersError:
            print(Fore.RED + """
            There are no candidates matching that search term.
            """ + Fore.RESET)
        else:
            if results:
                print(Fore.CYAN + '%s Total | Search Results:' % (results['totalFound']) + Fore.RESET)
                for r in results['content']:
                    print(Fore.MAGENTA + """
                    %s %s | %s
                    """ % (r['firstName'], r['lastName'], r['id'])
                    + Fore.RESET)
            else:
                print(Fore.RED + """
                There are no candidates matching that search term.
                """ + Fore.RESET)

        action = raw_input('Press enter to return to Candidate Management.')
        if action == '':
            manage_candidates(instance)

    elif selection == '2': # add candidate
        clear()
        print(Fore.GREEN + 'Current Instance: %s' % (instance['name']) + Fore.RESET)
        print(Fore.CYAN + 'Candidate Creation' + Fore.RESET)

        number = raw_input('Number of candidates to add: ')
        for _ in range(int(number)):
            candidate = Utility(instance=instance).create_candidate_json()
            
            try:
                response = api.CandidateAPI.create(candidate)
            except SmartRecruitersError:
                print(Fore.RED + """
                There was an error adding that candidate.
                """ + Fore.RESET)
            else:
                print(Fore.YELLOW + """
                Candidate added: %s %s
                """ % (
                    response['firstName'],
                    response['lastName']
                ) + Fore.RESET)
        
        action = raw_input('Press enter to return to Candidate Management.')
        if action == '':
            manage_candidates(instance)

    elif selection == '3': # add and assign candidate to job
        clear()
        print(Fore.GREEN + 'Current Instance: %s' % (instance['name']) + Fore.RESET)
        print(Fore.CYAN + 'Candidate Creation and Assignment' + Fore.RESET)

        job_id = raw_input('Job ID: ')
        number = raw_input('Number of candidates to add and assign: ')
        for _ in range(int(number)):
            candidate = Utility(instance=instance).create_candidate_json()
            
            try:
                response = api.CandidateAPI.assign(job_id, candidate)
            except SmartRecruitersError:
                print(Fore.RED + """
                There was an error adding and assigning that candidate.
                """ + Fore.RESET)
            else:
                print(Fore.YELLOW + """
                Candidate added: %s %s
                """ % (
                    response['firstName'],
                    response['lastName']
                ) + Fore.RESET)
        
        action = raw_input('Press enter to return to Candidate Management.')
        if action == '':
            manage_candidates(instance)

    elif selection == '4': # get candidate details
        clear()
        print(Fore.GREEN + 'Current Instance: %s' % (instance['name']) + Fore.RESET)
        print(Fore.CYAN + 'Candidate Info' + Fore.RESET)

        candidate_id= raw_input('Candidate ID: ')

        try:
            response = api.CandidateAPI.get(candidate_id)
        except SmartRecruitersError:
            print(Fore.RED + """
            That ID does not match a candidate.
            """ + Fore.RESET)
        except ValueError:
            print(Fore.RED + """
            Invalid input; try again.
            """ + Fore.RESET)
        else:
            print(Fore.YELLOW + """
            %s %s
            %s
            %s
            """ % (
                response['firstName'], response['lastName'],
                response['email'],
                'https://www.smartrecruiters.com/app/people/candidates/' + response['id']
            ) + Fore.RESET)

        action = raw_input('Press enter to return to Candidate Management.')
        if action == '':
            manage_candidates(instance)

    elif selection == '5':
        menu(instance)


if __name__ == '__main__': 
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(Fore.GREEN + 'Thanks for using smarty.py!' + Fore.RESET)
        print(Fore.LIGHTBLACK_EX + """finished with exit code 1""" + Fore.RESET)
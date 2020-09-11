# Author: Jose Oliveira
# Creation Date: Monday, July 20, 2020
# Modified Date: Wednesday, September 09, 2020
# Version: 2.0
# This scripts allows system administrators to modify users and groups.

import os
import pwd
import subprocess
import getpass
import crypt
import grp
from colorama import init
from termcolor import colored

# Convert a list to a string
def listToString(s):
    # Initialize an empty string
    str1 = ' '
    return (str1.join(s))

# Convert a list to a string with a comma
def listStringComma(s):
    # Initialize an empty string
    str1 = ','
    return (str1.join(s))

# Convert a list to a string with a comma and space after each index
def listStringCommaSpace(s):
    # Initialize an empty string
    str1 = ', '
    return (str1.join(s))

# Create a new user
def new_user():
    print ('This function will create a new user.')
    confirm = 'N'
    while confirm != 'Y':
        # Find all of the users created in the system
        users = str(subprocess.Popen(['cat /etc/passwd | cut -d: -f1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))

        # Create a list of the users
        usersList = []
        buff = []
        for c in users:
            if c == '\n':
                usersList.append(''.join(buff))
                buff = []
            else:
                buff.append(c)
        else:
            if buff:
                usersList.append(''.join(buff))

        # Find all of the groups created in the system
        groups = str(subprocess.Popen(['cat /etc/group | cut -d: -f1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))

        # Create a list of the groups
        groupsList = []
        buff = []
        for c in groups:
            if c == '\n':
                groupsList.append(''.join(buff))
                buff = []
            else:
                buff.append(c)
        else:
            if buff:
                groupsList.append(''.join(buff))

        print('\nThe following users exist: ' + colored(listStringCommaSpace(usersList), 'blue'))
        username = input('\nPlease enter the username to add: ')
 
        try:
            pwd.getpwnam(username)
            print('Sorry, the user "' + username + '" already exists. Please try another username.')
        except KeyError:
            fullname = input('Please enter the full name of the user: ')
            confirmUser = input('\nConfirm username "' + username + '"? (Y/N) ')
            confirmUser2 = confirmUser.upper()
            print()
            if confirmUser2 == 'Y':
                pmatch = 'N'
                while pmatch != '':
                    password = getpass.getpass()
                    password2 = getpass.getpass('Retype Password: ')
                    if password != password2:
                        print('\nSorry, password fields do not match. Please try again.\n')
                        pmatch = 'N'
                    elif password2 == '':
                        password2 = crypt.crypt('P@ssWord123')
                        if username in groupsList:
                            subprocess.run(['sudo', 'useradd', '-p', password2, '-c', fullname, '-g', username, username])
                        else:
                            subprocess.run(['sudo', 'useradd', '-p', password2, '-c', fullname, username])
                        print('\nThe user "' + username + '" was created successfully. The password is set to default.')
                        pmatch = ''
                        userAgain = input('\nWould you like to add another user? (Y/N) ')
                        userAgain2 = userAgain.upper()
                        if userAgain2 == 'Y':
                            confirm = 'N'
                        else:
                            print('-----------------------------------------------')
                            confirm = 'Y'
                            break
                    else:
                        password2 = crypt.crypt(password)
                        if username in groupsList:
                            subprocess.run(['sudo', 'useradd', '-p', password2, '-c', fullname, '-g', username, username])
                        else:
                            subprocess.run(['sudo', 'useradd', '-p', password2, '-c', fullname, username])
                        print('\nThe user "' + username + '" was created successfully.')
                        pmatch = ''
                        userAgain = input('\nWould you like to add another user? (Y/N) ')
                        userAgain2 = userAgain.upper()
                        if userAgain2 == 'Y':
                            confirm = 'N'
                        else:
                            print('-----------------------------------------------')
                            confirm = 'Y'
                            break
            else:
                userAgain = input('Would you like to add a different user instead? (Y/N) ')
                userAgain2 = userAgain.upper()
                if userAgain2 == 'Y':
                    confirm = 'N'
                else:
                    print('-----------------------------------------------')
                    confirm = 'Y'
                    break

#Change a user's password
def change_password():
    print('This function overwrites a user\'s password.')
    confirm = 'N'
    while confirm != 'Y':
        username = input('\nPlease enter the name of the user to change their password: ')
        try:
            pwd.getpwnam(username)
            pmatch = 'N'
            while pmatch != '':
                print()
                password = getpass.getpass()
                if password == '':
                    print('\nSorry, password cannot be empty. Please try again.\n')
                    pmatch = 'N'
                else:
                    password2 = getpass.getpass('Retype Password: ')
                    if password != password2:
                        print('\nSorry, password fields do not match. Please try again.\n')
                        pmatch = 'N'
                    else:
                        password2 = crypt.crypt(password2)
                        subprocess.run(['sudo', 'usermod', '-p', password2,  username])
                        print('\nThe user "' + username + '\'s" password was updated successfully.')
                        pmatch = ''
                        userAgain = input('\nWould you like to change another user\'s password? (Y/N) ')
                        userAgain2 = userAgain.upper()
                        if userAgain2 == 'Y':
                            confirm = 'N'
                        else:
                            print('-----------------------------------------------')
                            confirm = 'Y'
                            break
        except:
            print('Sorry, the user "' + username + '" does not exist. Please try another username.')


# Remove a user
def remove_user():
    print('This function will remove a user.')
    confirm = 'N'
    while confirm != 'Y':
        # Find all of the users created in the system
        users = str(subprocess.Popen(['cat /etc/passwd | cut -d: -f1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))

        # Create a list of the users
        usersList = []
        buff = []
        for c in users:
            if c == '\n':
                usersList.append(''.join(buff))
                buff = []
            else:
                buff.append(c)
        else:
            if buff:
                usersList.append(''.join(buff))

        whoami = str(subprocess.Popen(['whoami'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))
        whoami = whoami.strip('\n')
        who = str(subprocess.Popen(['who | cut -d: -f1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))
        who = who.split('\n')
        who = ' '.join(who).split()
        
        print('\nThe following users exist: ' + colored(listStringCommaSpace(usersList), 'blue'))
        username = input('\nPlease enter the name of the user to remove: ')
        if whoami == username:
            print('Sorry, you cannot remove user "' + username + '" while logged in as this user.\nPlease try another username.')
        elif username in who:
            print('Sorry, you cannot remove user "' + username + '" because they are currently logged in.\nPlease, try again later.')
        else:
            try:
                pwd.getpwnam(username)
                # List the group(s) the user belongs to
                userGroups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
                gid = pwd.getpwnam(username).pw_gid
                userGroups.append(grp.getgrgid(gid).gr_name)
                userGroups.sort()
                print('The user "' + username + '" is a member of the following group(s): ' + colored(listStringCommaSpace(userGroups), 'blue'))
                confirmRemove = input('\nConfirm username "' + username + '"? (Y/N) ')
                confirmRemove2  = confirmRemove.upper()
                if confirmRemove2 == 'Y':
                    subprocess.run(['sudo', 'killall', '-u', username])
                    subprocess.run(['sudo', 'userdel', '-r', username])
                    print('\nThe user "' + username + '" was removed successfully.')
                    removeAgain = input('\nWould you like to remove another user? (Y/N) ')
                    removeAgain2 = removeAgain.upper()
                    if removeAgain2 == 'Y':
                        confirm = 'N'
                    else:
                        print('-----------------------------------------------')
                        confirm = 'Y'
                        break
                else:
                    removeAgain = input('\nWould you like to remove a different user instead? (Y/N) ')
                    removeAgain2 = removeAgain.upper()
                    if removeAgain2 == 'Y':
                        confirm = 'N'
                    else:
                        print('-----------------------------------------------')
                        confirm = 'Y'
                        break
            except KeyError:
                print('Sorry, the user "' + username + '" doesn\'t exist. Please try another username.')

# Add a group
def add_group():
    print('This function will add a secondary group to the system.')
    confirm = 'N'
    while confirm != 'Y':
        # Find all of the groups created in the system
        groups = str(subprocess.Popen(['cat /etc/group | cut -d: -f1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))

        # Create a list of the groups
        groupsList = []
        buff = []
        for c in groups:
            if c == '\n':
                groupsList.append(''.join(buff))
                buff = []
            else:
                buff.append(c)
        else:
            if buff:
                groupsList.append(''.join(buff))
        
        print('\nThe following group(s) exist in the system:\n' + colored(listStringCommaSpace(groupsList), 'green'))

        groupname = input('\nPlease enter the group(s) to add: ')
        groupname = groupname.split(' ')
        groupname = list(dict.fromkeys(groupname)) # Remove duplicates

        existentGroup = [i for i in groupname if i in groupsList]

        try:
            if len(existentGroup) > 0:
                raise KeyError('GroupAlreadyExists')
            confirmRemove = input('\nConfirm add group(s) "' + listStringCommaSpace(groupname) + '"? (Y/N) ')
            confirmRemove2  = confirmRemove.upper()
            if confirmRemove2 == 'Y':
                for x in groupname:
                    os.system('sudo groupadd ' + x)
                    print('Group: ' + colored(x, 'green') + ' was successfully created.')
                addAgain = input('\nWould you like to add another group(s)? (Y/N) ')
                addAgain2 = addAgain.upper()
                if addAgain2 == 'Y':
                    confirm = 'N'
                else:
                    print('-----------------------------------------------')
                    confirm = 'Y'
                    break
            else:
                addAgain = input('\nWould you like to add a different group(s) instead? (Y/N) ')
                addAgain2 = addAgain.upper()
                if addAgain2 == 'Y':
                    confirm = 'N'
                else:
                    print('-----------------------------------------------')
                    confirm = 'Y'
                    break
        except KeyError:
            print('Sorry, the group(s) "' + colored(listStringCommaSpace(existentGroup), 'green') + '" already exists. Please try another group.')

# Add a user to a group or groups
def add_user_to_group():
    print('This function will add a user to a secondary group(s).')
    confirm = 'N'
    while confirm != 'Y':
        username = input('\nPlease enter the user that you wish to add to a group(s): ')
        try:
            # Checks if the users exists and confirm user
            pwd.getpwnam(username)

            # List the group(s) the user belongs to
            userGroups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            gid = pwd.getpwnam(username).pw_gid
            userGroups.append(grp.getgrgid(gid).gr_name)
            userGroups.sort()
            print('The user "' + username + '" is a member of the following group(s): ' + colored(listStringCommaSpace(userGroups), 'blue'))

            userConfirm = input('\nConfirm username "' + username + '"? (Y/N) ')
            userConfirm  = userConfirm.upper()
            if userConfirm == 'Y':
                # Find all of the groups created in the system
                groups = str(subprocess.Popen(['cat /etc/group | cut -d: -f1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))
            
                # Create a list of the groups
                groupsList = []
                buff = []
                for c in groups:
                    if c == '\n':
                        groupsList.append(''.join(buff))
                        buff = []
                    else:
                        buff.append(c)
                else:
                    if buff:
                        groupsList.append(''.join(buff))

                # Display the available group(s) except the ones the user already belongs to
                nonUserGroups = [i for i in groupsList + userGroups if i not in userGroups]
                print('The following group(s) exist in the system:\n' + colored(listStringCommaSpace(nonUserGroups), 'green'))

                # User inputs the group(s) and creates a list
                chosenGroups = input('\nPlease list the group(s) you would like to add "' + username + '" to: ')
                chosenGroups = chosenGroups.split(' ')
            
                # Check if the user belongs to one of the group(s)
                userGroups = [i for i in userGroups if i in chosenGroups]
                userGroups = list(dict.fromkeys(userGroups)) # Remove duplicates

                # Check if the group(s) already exist
                existGroups = [i for i in groupsList if i in chosenGroups and i not in userGroups]
                existGroups = list(dict.fromkeys(existGroups)) # Remove duplicates

                # Check if the group(s) does not exist
                nonExistGroups = [i for i in groupsList + chosenGroups if i not in groupsList]
                nonExistGroups = list(dict.fromkeys(nonExistGroups)) # Remove duplicates

                if userGroups:
                    print('\nThe following group(s) will be disregarded: ' + colored(listStringCommaSpace(userGroups), 'blue'))
                else:
                    print()

                if existGroups:
                    print('The following groups exist: ' + colored(listStringCommaSpace(existGroups), 'green'))

                if existGroups and nonExistGroups:
                    print()

                if nonExistGroups:
                    print('The following group(s) do not exist: ' + colored(listStringCommaSpace(nonExistGroups), 'red'))
                    while True:
                        createGroups = input('Would you like to create the group(s) mentioned above? (Y/N): ')
                        createGroups = createGroups.upper()
                        if createGroups == 'Y':
                            for x in nonExistGroups:
                                os.system('sudo groupadd ' + x)
                                print('Group: ' + colored(x, 'green') + ' was successfully created.')
                            groupsCreated = True
                            break
                        else:
                            groupsCreated = False
                            break
                else:
                    groupsCreated = False

                if existGroups and nonExistGroups and groupsCreated == True:
                    groupString = existGroups + nonExistGroups
                elif existGroups and not nonExistGroups and groupsCreated == False:
                    groupString = existGroups
                elif not existGroups and nonExistGroups and groupsCreated == True:
                    groupString = nonExistGroups
                else:
                    print('No changes were made to user "' + username + '"')
                    print('-----------------------------------------------')                                
                    confirm = 'Y'
                    break

                if groupString:
                    while True:
                        addGroups = input('\nConfirm add user "' + username + '" to the group(s) "' + colored(listStringCommaSpace(groupString), 'green') + '" ? (Y/N) ')
                        addGroups = addGroups.upper()
                        if addGroups == 'Y':
                            if len(groupString) == 1:
                                os.system('sudo usermod -aG ' + listToString(groupString) + ' ' + username)
                                print('The user "' + username + '" was successfully added to the group(s): ' + colored(listStringCommaSpace(groupString), 'green'))
                            else:
                                os.system('sudo usermod -aG ' + listStringComma(groupString) + ' ' + username)
                                print('The user "' + username + '" was successfully added to the group(s): ' + colored(listStringCommaSpace(groupString), 'green'))
                            addAgain = input('\nWould you like to add another user to a group? (Y/N) ')
                            addAgain2 = addAgain.upper()
                            if addAgain2 == 'Y':
                                confirm = 'N'
                                break
                            else:
                                print('-----------------------------------------------')
                                confirm = 'Y'
                                break
                        else:
                            print('No changes were made to user "' + username + '"')
                            print('-----------------------------------------------')
                            confirm = 'Y'
                            break
            else:
                addAgain = input('\nWould you like to add a different user to a group instead? (Y/N) ')
                addAgain2 = addAgain.upper()
                if addAgain2 == 'Y':
                    confirm = 'N'
                else:
                    print('-----------------------------------------------')
                    confirm = 'Y'
                    break
        except KeyError:
            print('Sorry, the user "' + username + '" does not exist. Please try another username.')

# Remove a user from a secondary group
def remove_user_from_group():
    print('This function will remove a user from a secondary group(s).')
    confirm = 'N'
    exit = ''
    while confirm != 'Y':
        whoami = str(subprocess.Popen(['whoami'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))
        whoami = whoami.strip('\n')
        who = str(subprocess.Popen(['who | cut -d: -f1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))
        who = who.split('\n')
        who = ' '.join(who).split()
        username = input('\nPlease enter the name of the user to remove from a group(s): ')
        if whoami == username:
            print('Sorry, you cannot modify group(s) of user "' + username + '" while logged in as this user.\nPlease try another username.')
        elif username in who:
            print('Sorry, you cannot modify group(s) of user "' + username + '" because they are currently logged in.\nPlease, try again later.')
        else:
            try:
                pwd.getpwnam(username)
                # List the group(s) the user belongs to
                userGroups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
                userGroups.sort()
                if len(userGroups) < 1:
                    raise KeyError('NoSecondaryGroups')
                print('The user "' + username + '" is a member of the following group(s): ' + colored(listStringCommaSpace(userGroups), 'blue'))
                confirmRemove = input('\nConfirm username "' + username + '"? (Y/N) ')
                confirmRemove2  = confirmRemove.upper()
                if confirmRemove2 == 'Y':
                    noGroup = 'N'
                    while noGroup != 'Y':
                        groupName = input('\nPlease enter the group(s) to remove the user "' + username + '" from: ')
                        groups = groupName.split(' ')

                        for i in groups:
                            if i in userGroups:
                                # Create a list of all the groups except the one to remove the user from
                                groupsToKeep = [i for i in userGroups if i not in groups]
                                if len(groupsToKeep) < 1:
                                    os.system('sudo usermod -G "" ' + username)
                                    print('\nThe user "' + username + '" was removed from the group(s) "' + listToString(groups) + '" successfully.')
                                else:
                                    os.system('sudo usermod -G ' + listStringComma(groupsToKeep) + ' ' + username)
                                    print('\nThe user "' + username + '" was removed from the group(s) "' + listStringCommaSpace(groups) + '" successfully.')
                                removeAgain = input('\nWould you like to remove another user from a group(s)? (Y/N) ')
                                removeAgain2 = removeAgain.upper()
                                if removeAgain2 == 'Y':
                                    exit = 'N'
                                    break
                                else:
                                    print('-----------------------------------------------')
                                    exit = 'Y'
                                    break
                            else:
                                print('Sorry, user "' + username + '" doesn\'t belong to the group(s) "' + listStringCommaSpace(groups) + '." Please try another group(s).')
                                break
                                noGroup = 'Y'
                        if exit == 'Y' or exit == 'N':
                            noGroup = 'Y'
                            break
                    if exit == 'Y':
                        confirm = 'Y'
                        break
                    else:
                        confirm = 'N'
                else:
                    removeAgain = input('\nWould you like to remove a different user from a group(s) instead? (Y/N) ')
                    removeAgain2 = removeAgain.upper()
                    if removeAgain2 == 'Y':
                        confirm = 'N'
                    else:
                        print('-----------------------------------------------')
                        confirm = 'Y'
                        break
            except KeyError:
                print('Sorry, the user "' + username + '" doesn\'t belong to any secondary group(s). Please try another username.')

# Remove a group
def remove_group():
    print('This function will remove a secondary group from the system.')
    confirm = 'N'
    while confirm != 'Y':
        # Find all of the groups created in the system
        groups = str(subprocess.Popen(['cat /etc/group | cut -d: -f1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))

        # Create a list of the groups
        groupsList = []
        buff = []
        for c in groups:
            if c == '\n':
                groupsList.append(''.join(buff))
                buff = []
            else:
                buff.append(c)
        else:
            if buff:
                groupsList.append(''.join(buff))
        
        # Find all of user's primary group Id
        primaryId = str(subprocess.Popen(['cat /etc/passwd | cut -d: -f4'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))

        # Create a list of the primary group Id's
        primaryIdList = []
        buff = []
        for c in primaryId:
            if c == '\n':
                primaryIdList.append(''.join(buff))
                buff = []
            else:
                buff.append(c)
        else:
            if buff:
                primaryIdList.append(''.join(buff))

        # Find all of the groups Id's created in the system
        groupId = str(subprocess.Popen(['cat /etc/group | cut -d: -f3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))

        # Create a list of the group Id's
        groupIdList = []
        buff = []
        for c in groupId:
            if c == '\n':
                groupIdList.append(''.join(buff))
                buff = []
            else:
                buff.append(c)
        else:
            if buff:
                groupIdList.append(''.join(buff))

        # Make a new list of group Id's only for secondary groups
        secGroupId = [i for i in groupIdList if i in groupIdList and i not in primaryIdList]

        secGroupList = []
        for x in secGroupId:
            secGroupCommand = 'getent group ' + x + ' | cut -d: -f1'
            secGroup = str(subprocess.Popen([secGroupCommand], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))
            for c in secGroup:
                if c == '\n':
                    secGroupList.append(''.join(buff))
                    buff = []
                else:
                    buff.append(c)
            else:
                if buff:
                    secGroupList.append(''.join(buff))

        # Get the username of the current user
        whoami = str(subprocess.Popen(['whoami'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))
        whoami = whoami.strip('\n')

        # Get a list of users currently logged in, make a list and remove any empty strings
        who = str(subprocess.Popen(['who | cut -d: -f1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))
        who = who.split('\n')
        who = ' '.join(who).split()

        print('\nThe following groups are available to be removed:\n' + colored(listStringCommaSpace(secGroupList), 'green'))

        # User inputs group name(s) to remove
        groupname = input('\nPlease enter the group to remove: ')

        groupMemberCommand = 'getent group ' + groupname + ' | cut -d: -f4'
        groupMember = str(subprocess.Popen([groupMemberCommand], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8'))
        groupMember = groupMember.split(',')
        groupMember = ' '.join(groupMember).split()
        
        loggedIn = []
        for x in who:
            if x in groupMember:
               loggedIn.append(x)

        if groupname not in secGroupList and groupname in groupsList:
            print('Sorry, you cannot remove a primary group.\nPlease try a secondary group.')
        elif whoami in groupMember:
            print('Sorry, you cannot remove group of user "' + whoami + '" while logged in as this user.\nPlease try another group.')
        elif len(loggedIn) > 0:
            print('Sorry, you cannot remove group of user(s) "' + listStringCommaSpace(loggedIn) + '" because they are currently logged in.\nPlease, try again later.')
        else:
            try:
                if groupname not in secGroupList and groupname not in groupsList:
                    raise KeyError('NoGroup')
                if len(groupMember) < 1:
                    print('The group "' + groupname + '" has no members.')
                else:
                    print('The following user(s) belong to the group "' + groupname + '": ' + colored(listStringCommaSpace(groupMember), 'blue'))
                confirmRemove = input('\nConfirm remove group "' + groupname + '"? (Y/N) ')
                confirmRemove2  = confirmRemove.upper()
                if confirmRemove2 == 'Y':
                    subprocess.run(['sudo', 'groupdel', groupname])
                    print('\nThe group "' + groupname + '" was removed successfully.')
                    removeAgain = input('\nWould you like to remove another secondary group? (Y/N) ')
                    removeAgain2 = removeAgain.upper()
                    if removeAgain2 == 'Y':
                        confirm = 'N'
                    else:
                        print('-----------------------------------------------')
                        confirm = 'Y'
                        break
                else:
                    removeAgain = input('\nWould you like to remove a different group instead? (Y/N) ')
                    removeAgain2 = removeAgain.upper()
                    if removeAgain2 == 'Y':
                        confirm = 'N'
                    else:
                        print('-----------------------------------------------')
                        confirm = 'Y'
                        break
            except KeyError:
                print('Sorry, the group "' + groupname + '" doesn\'t exist. Please try another group.')

# Run the functions as a program
def users():
    print('Welcome! This program allows you to modify users and groups.\n' + colored('*Please note: You must have sudo credentials to make modifications.', 'red'))
    print('=======================================================================')
    program = 'N'
    exit = ''
    while program != 'Y':
        print('\nPlease choose which function you would like to perform.')
        print('Enter "q" to exit this program.')
        print('-----------------------------------------------')
        print('1. Add a new user')
        print('2. Change a user\'s password')
        print('3. Remove a user')
        print('4. Add a secondary group')
        print('5. Add a user to a secondary group(s)')
        print('6. Remove a user from a secondary group(s)')
        print('7. Remove a secondary group')
        function = 'N'
        while function != 'Y':
            choice = input(colored('\nPlease enter your input: ', 'green'))
            if choice == '1':
                print('-----------------------------------------------')
                new_user()
                answer = input(colored('\nWould you like to perform another function? (Y/N) ', 'green'))
                answer = answer.upper()
                if answer == 'Y':
                    break
                    program = 'N'
                else:
                    exit = 'Y'
                    break
            elif choice == '2':
                print('-----------------------------------------------')
                change_password()
                answer = input(colored('\nWould you like to perform another function? (Y/N) ', 'green'))
                answer = answer.upper()
                if answer == 'Y':
                    break
                    program = 'N'
                else:
                    exit = 'Y'
                    break
            elif choice == '3':
                print('-----------------------------------------------')
                remove_user()
                answer = input(colored('\nWould you like to perform another function? (Y/N) ', 'green'))
                answer = answer.upper()
                if answer == 'Y':
                    break
                    program = 'N'
                else:
                    exit = 'Y'
                    break
            elif choice == '4':
                print('-----------------------------------------------')
                add_group()
                answer = input(colored('\nWould you like to perform another function? (Y/N) ', 'green'))
                answer = answer.upper()
                if answer == 'Y':
                    break
                    program = 'N'
                else:
                    exit = 'Y'
                    break
            elif choice == '5':
                print('-----------------------------------------------')
                add_user_to_group()
                answer = input(colored('\nWould you like to perform another function? (Y/N) ', 'green'))
                answer = answer.upper()
                if answer == 'Y':
                    break
                    program = 'N'
                else:
                    exit = 'Y'
                    break
            elif choice == '6':
                print('-----------------------------------------------')
                remove_user_from_group()
                answer = input(colored('\nWould you like to perform another function? (Y/N) ', 'green'))
                answer = answer.upper()
                if answer == 'Y':
                    break
                    program = 'N'
                else:
                    exit = 'Y'
                    break
            elif choice == '7':
                print('-----------------------------------------------')
                remove_group()
                answer = input(colored('\nWould you like to perform another function? (Y/N) ', 'green'))
                answer = answer.upper()
                if answer == 'Y':
                    break
                    program = 'N'
                else:
                    exit = 'Y'
                    break
            elif choice == 'q':
                exit = 'Y'
                break
            else:
                print('Sorry, that isn\'t a valid response. Please try again.')
                function = 'N'
        if exit == 'Y':
            break

users()

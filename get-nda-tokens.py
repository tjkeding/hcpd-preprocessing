#!/usr/bin/python3
# coding: utf-8

# =======================================================================================================================
# GENERATING NDA TOKENS for DOWNLOADING DATA from HCPD REPOSITORY
# Written by Taylor J. Keding (tjkeding@gmail.com)
# Last Updated: 06.04.20
# =======================================================================================================================
# -----------------------------------------------------------------------------------------------------------------------
# IMPORTS:
# -----------------------------------------------------------------------------------------------------------------------

from nda_aws_token_generator import *
import getpass
import os
from configparser import ConfigParser

# -----------------------------------------------------------------------------------------------------------------------
# FUNCTIONS:
# -----------------------------------------------------------------------------------------------------------------------

def getSignInCreds():

    # Prompt user for username and save
    try:
        userName = getpass.getuser("User Name: ")
    except:
        print("Incorrect username."")
        sys.exit()

    # Prompt user for password and save
    try:
        passWord = getpass.getpass("Password: ")
    except:
        print("Incorrect password.")
        sys.exit()

    return [userName,passWord]

# -----------------------------------------------------------------------------------------------------------------------
# MAIN:
# -----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # Get NDA sign-in credentials from user
    creds = getSignInCreds()
    username  = creds[0]
    password  = creds[1]

    # Get tokens from the NDA credentials
    web_service_url = 'https://nda.nih.gov/DataManager/dataManager'
    generator = NDATokenGenerator(web_service_url)
    token = generator.generate_token(username, password)

    # Read .aws/credentials from the user's HOME directory, add a NDA profile, and update with credentials
    parser = ConfigParser()
    parser.read(os.path.expanduser('~/.aws/credentials'))
    if not parser.has_section('default'):
        parser.add_section('default')
    parser.set('default', 'aws_access_key_id', token.access_key)
    parser.set('default', 'aws_secret_access_key', token.secret_key)
    parser.set('default', 'aws_session_token', token.session)
    with open (os.path.expanduser('~/.aws/credentials'), 'w') as configfile:
        parser.write(configfile)

    # Add explicit export commands for the tokens (often necessary)
    # This will only work on linux and mac operating systems
    command1 = str("export AWS_ACCESS_KEY_ID="+str(token.access_key))
    command2 = str("export AWS_SECRET_ACCESS_KEY="+str(token.secret_key))
    command3 = str("export AWS_SESSION_TOKEN="+str(token.session))
    os.system(command1)
    os.system(command2)
    os.system(command3)

    # Print the tokens to the command line
    print('aws_access_key_id=%s\n'
         'aws_secret_access_key=%s\n'
          'aws_session_token=%s\n'
          'expiration=%s\n'
          %(token.access_key,
            token.secret_key,
            token.session,
            token.expiration)
          )

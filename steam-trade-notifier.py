#!/usr/bin/env python3

# File name: steam-trade-notifier.py
# Author: Rafa Marcen
# Date created: 25/10/2014
# Date last modified: 25/10/2014
# Purpose: Send an e-mail notification when a Steam trade offer is accepted or
# received.
# Documentation URL:
# https://developer.valvesoftware.com/wiki/Steam_Web_API/IEconService

# Set these before running this script:
STEAM_API_KEY = 'YOUR_STEAM_API_KEY'
STEAM_PROFILE = 'PROFILE_NAME'
SMTP_SERVER = 'EMAIL_SMTP_SERVER'
SMTP_PORT = 465
SMTP_USERNAME = 'YOUR_EMAIL'
SMTP_PASSWORD = 'YOUR_EMAIL_PASSWORD'
RECIPIENT_ADDRESS = 'YOUR_EMAIL'

import json
import smtplib
import time
import urllib.request

DEBUG = False

def call_method(service, method, version, key, userId=None, params=None):
    url = 'https://api.steampowered.com/' + \
          '{service}/{method}/v{v}/?key={key}'.format(
              service=service,
              method = method,
              v = version,
              key = key)

    # If a User ID was given
    if userId != None:
        # Append the user ID
        url += '&steamid=' + userId

    # Specify JSON as the format
    url += '&format=json'

    if params != None:
        # Add each parameter
        for k, v in params.items():
            url += '&' + str(k) + '=' + str(v)
           
    if DEBUG:
        print(url)

    # Get the HTTP response
    response = urllib.request.urlopen(url)

    # Decode the binary response into text
    encoding = response.headers.get_content_charset()
    responseText = response.read().decode(encoding)

    return json.loads(responseText)['response']

def create_email_body(response):
    numAccepted = response['pending_sent_count']
    numReceived = response['pending_received_count']
    body = ''

    if numReceived > 0:
        body += '{} new offer'.format(numReceived)
        if numReceived != 1:
            body += 's'
        body += '\r\n'

    if numAccepted > 0:
        body += str(numAccepted)
        body += ' offer'
        if numAccepted == 1:
            body += ' was'
        else:
            body += 's were'
        body += ' accepted\r\n'

    if body != '':
        body += '\r\n'
        body += 'https://steamcommunity.com/id/' + STEAM_PROFILE + \
                '/tradeoffers/'

        return body
    else:
        return None

def send_notification_email(to, subject, body):
    session = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    #session.starttls()
    session.ehlo()
    session.login(SMTP_USERNAME, SMTP_PASSWORD)

    headers = '\r\n'.join(
        ['from: ' + SMTP_USERNAME,
         'subject: ' + subject,
         'to: ' + to,
         'mime-version: 1.0',
         'content-type: text/plain'])

    content = headers + '\r\n\r\n' + body
    session.sendmail(SMTP_USERNAME, to, content)


# Get the timestamp from 6 minutes ago (this script must be run more often
# than every 6 minutes or we will miss updates)
timestamp = int(time.time()) - (6 * 60)

response = call_method('IEconService',
                       'GetTradeOffersSummary', '1',
                       STEAM_API_KEY,
                       None,
                       {'time_last_visit': timestamp})

if DEBUG:
    print(response)

body = create_email_body(response)
print(body)
if body != None:
    send_notification_email(RECIPIENT_ADDRESS,'Steam Trade Notification', body)
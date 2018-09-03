# -*- coding: UTF-8 -*-

# v1.0
# author: ashpotak
# 18.07.2018 
# 
# script for transfering birthdays of besties of lbg lviv from csv file to google calendar
# need to be improved:
# - coding of input data (smth wrong with it)
# - normal reccuring events (i don't know how to do events reccuring yearly)
# 
# need to be fixed:
# - problem with birthdays in 29 of February - they cause an error and stop script 
# 
# nice to be added:
# - transfering directly from google spreadsheets
# - triggering on adding new member to infobook


from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import client, tools
from oauth2client.file import Storage
import datetime

import csv
 
FILENAME = "infobook.csv"

besties = []

def dateOptimizer(date):
      date = date.split('.')
      newdate = '2018-' + date[1] + '-' + date[0] #kostyl' is there
      return newdate

def bestieOptimizer(bestie):
      bestie[0] = bestie[0] + ' ' + bestie[1]
      bestie.pop(1)
      bestie[1] = dateOptimizer(bestie[1])
      return bestie


with open(FILENAME, "r", newline="") as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        row = row[0].split(",")
        besties.append([row[0],row[1],row[2]])

#print(besties)

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

for bestie in besties:
      bestie = bestieOptimizer(bestie)
      event = {
        'summary': bestie[0],
        'start': {
          'date': bestie[1],
        },
        'end': {
          'date': bestie[1],
        },
      }
      #print(event)
      event = service.events().insert(calendarId='nmmvejgv1h6r9mef3mfh8uc8ik@group.calendar.google.com', body=event).execute()
      print('Event created: %s' % (event.get('htmlLink')))
      
  
#print(event['summary'])

#bestieOptimizer(besties[0])
import os
from twilio.rest import Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import time

print('welcome to the medicine compliance program. \
This program helps you keep track of your medicine \
compliance by reminding you on your phone and gathers \
information on whether you take your medicine or not.')

#inputs
def get_inputs():
    run = True
    while run == True:
        try:
            hours = float(input('enter the amount of hours between each\
 reminder (ex: 7.5 for 7 hours and a half): '))
            while hours < 0.1:
                hours = float(input('too little time between reminders.\
 Enter another time: '))
            return hours
        except:
            print('numbers only.')

def get_seconds(hours):
    sec = hours*3600
    return sec

def log_data(med_taken, index, reminder_num):
    scope = ['https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.\
    from_json_keyfile_name('medicineCompliance-ce5dba463e74.json', scope)

    client = gspread.authorize(creds)

    sheet = client.open('Medicine Compliance').sheet1

    #data = sheet.get_all_records()
    #print(data)

    index += 1
    reminder = 'reminder ' + str(reminder_num)

    row = [reminder, med_taken]
    sheet.insert_row(row, index)
    reminder_num += 1
    return index, reminder_num

def sendMessage(account_sid, auth_token):
        client = Client(account_sid, auth_token)

        client.messages \
                        .create(
                            body= 'REMINDER: take medicine and go\
 to the computer to say if you took it or not.',
                            from_='+14243177481',
                            to='+13105925301'
                        )

# main --------------------------

hours = get_inputs()
sec = get_seconds(hours)
#print(sec)
med_taken_list = ['yes', 'no']
reminder_num = 1
index = 1
run = True
while run == True:
    time.sleep(10)
    account_sid = 'AC6ade5f993b29faf330a9e9ac61c74ab'
    auth_token = 'e8fa75993e3cb6583e174658ee036903'

    sendMessage(account_sid, auth_token)

    med_taken = str(input('Have you taken your medicine or not ("yes", "no"): '))
    while med_taken not in med_taken_list:
        med_taken = str(input('Must be "yes" or "no": )'))
    index, reminder_num = log_data(med_taken, index, reminder_num)
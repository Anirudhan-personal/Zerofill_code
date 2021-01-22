from flask import Flask, render_template, request
from datetime import datetime
import random

app = Flask(__name__)
global langOption_V
langOption_V  = 0 # for english, 1 for Hindi, and 2 for Kannada

import serial
import time



global COUNTS
COUNTS = [0, 0, 0]

def validate_number(number):
   Valid = False

   VALID_INITIALS = ['6', '7','8','9']
   num_str = str(number)
   if(len(num_str) ==10):
      if(num_str.isnumeric()):
         if(num_str[0] in VALID_INITIALS):
            Valid = True

   return Valid


@app.route('/')
def landing_page():
   return render_template('landing_page.html')

@app.route('/index')  
def index():
   print ('in landing page')
   global langOption_V

   User_detection_string = ser.readline()
   print ('checking')
   langOption_V  = 0 # for english, 1 for Hindi, and 2 for Kannada
   User_detection_string = ser.readline().strip()
   print("String accepted", User_detection_string)
   if (User_detection_string == b"User:Null:end:"):
      print ('IN PROGRESS')
      return render_template('index.html')
   else:
      return render_template('landing_page.html')


@app.route('/enterMobile/<int:langOption>')
def enterMobile(langOption):
   global langOption_V
   langOption_V = langOption
   errorMessage = False
   return render_template('enterMobile.html', langOption=langOption_V, errorMessage=errorMessage)


@app.route('/enterOTP', methods=['POST'])
def enterOTP():
   global langOption_V
   mobileNo = request.form['mobNumber']
   print ('Got number: ', mobileNo)
   
   # mobile number validation
   VALID = validate_number(mobileNo)

   if VALID:
      return render_template('otpPage.html', langOption=langOption_V)
   else:
      errorMessage = True
      return render_template('enterMobile.html', langOption=langOption_V, errorMessage=errorMessage)



@app.route('/welcomePopup', methods=['POST'])
def welcomePopup():
   global langOption_V
   otp_received = request.form['otp']
   print ('Got OTP: ', otp_received)
   #controller is activated
   ser.write("Monitor:Null:end:".encode())
   return render_template('welcomePopup.html', langOption=langOption_V)

@app.route('/enterMain')
def enterMain():
   global langOption_V, COUNTS

   object_detection_string = ser.readline().strip()
   print(object_detection_string)
   if (object_detection_string == b"Object:1:end:" or object_detection_string == b"Object:2:end:" or object_detection_string == b"Object:3:end:"):
      if object_detection_string == b"Object:1:end:" :
         COUNTS[0]+=1
         ser.write("Object_Ack:Null:end:".encode())
      elif object_detection_string == b"Object:2:end:" :
         # click picture
         COUNTS[1]+=1
         ser.write("Object_Ack:Null:end:".encode())
      else:
         # click picture
         COUNTS[2]+=1
         ser.write("Object_Ack:Null:end:".encode())



   return render_template('mainSession.html', langOption=langOption_V, counts=COUNTS)

@app.route('/confirmPage')
def confirmPage():
   global langOption_V,COUNTS

   return render_template('confirmPage.html', langOption=langOption_V, total_credits = sum(COUNTS))

@app.route('/thanksPopup')
def thanksPopup():
   global langOption_V
   return render_template('thanksPopup.html', langOption=langOption_V)


@app.route('/redirectWelcome')
def redirectWelcome():
   global langOption_V, COUNTS
   ser.write("End:Null:end".encode())
   COUNTS = [0, 0, 0]
   return render_template('landing_page.html', langOption=langOption_V)


if __name__ == '__main__':
   print("test editing in git hub")
   ser = serial.Serial('COM10', 9600)
   app.run(port=10)

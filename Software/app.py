# Raspberry Pi School Bell Web System V2
from calendar import week
import threading
import time
import datetime
from gpiozero import LED, Button
from wsgiref.util import request_uri
from flask import Flask, render_template, request, url_for, redirect
import socket
from tinydb import TinyDB, Query
import I2C_LCD_driver

##################################################
#### Create connection with the database, and get
#### the secret key for changing ring times
##################################################
#/home/tszvono/school-bell-web-sys-V2
db = TinyDB('/srv/coffeebell/Software/db.json')
q = Query()
secretkey = db.get(q.type == 'secretkey').get('key')

##################################################
#### Get current ip address for displaying on LCD
##################################################
def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

#################################################################
#### Bell relay switcher, used to activate the raspberry pi
#### pins, which then activate the relay that activates the bell
#################################################################
def bell_relay_Switcher():
    relay = LED(26)
    switch_saturday = Button(23)
    switch_sunday = Button(24)
    relay.off()
    while(True):
        try:
            localpayload = payload
            e = datetime.datetime.now()
            for el in localpayload:
                weekday = e.weekday()
                # if it isnt saturday or sunday, ring regularly 
                if weekday != 5 or weekday != 6:
                    if e.hour == el[0]:
                        if e.minute == el[1]:
                            print("JACKPOT")
                            relay.on()
                            time.sleep(4)
                            relay.off()
                            time.sleep(60)
                # WORK IN PROGRESS
                # if its saturday, check if switch is set to ring on saturday
                if weekday == 5:
                    if switch_saturday.is_pressed:
                        pass
                # if its sunday, check if switch is set to ring on sunday 
                if weekday == 6:
                    if switch_sunday.is_pressed:
                        pass
                time.sleep(1)

        except Exception as error:
            print("ERROR while in bell relay switcher function")
            print(error)
            pass

#####################################################
#### LCD Interface, used to print useful information
#### to the consumer
#####################################################
def lcd_interface():
    mylcd = I2C_LCD_driver.lcd()
    try:
        ipaddress = extract_ip()
    except:
        pass
    while(True):
        try:
            mylcd.lcd_display_string("Server Online!", 1)
            e = datetime.datetime.now()
            current_time = str("Time: ")
            if e.hour <= 9:
                current_time += "0" + str(e.hour)
            else:
                current_time += str(e.hour)
            current_time += ":"
            if e.minute <= 9:
                current_time += "0" + str(e.minute)
            else:
                current_time += str(e.minute)
            mylcd.lcd_display_string(current_time, 2)
            time.sleep(5)
            mylcd.lcd_clear()

            mylcd.lcd_display_string("Connect to", 1)
            mylcd.lcd_display_string("tszvono.local", 2)
            time.sleep(5)
            mylcd.lcd_clear()
            if ipaddress:
                mylcd.lcd_display_string("IP:", 1)
                mylcd.lcd_display_string(ipaddress, 2)
                time.sleep(5)
                mylcd.lcd_clear()
        except Exception as error:
            print("ERROR while in lcd_interface function")
            print(error)
            pass

####################################################
#### Define functions as threads so they can run in
#### semi-parallel with the webserver.
####################################################
bell_relay_Switcher_THREAD = threading.Thread(target=bell_relay_Switcher, daemon=True)
lcd_interface_THREAD = threading.Thread(target=lcd_interface, daemon=True)

#######################################################
#### Flask webserver code. This is used as a website
#### to change the ring times easily by a consumer.
#######################################################
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/incorrectkey')
def incorrectkey():
    return render_template('incorrectkey.html')

@app.route('/timechange', methods=('GET', 'POST'))
def timechange():

    #if user wants to recieve form, return form
    if request.method == 'GET':
        return render_template('timechange.html')

    #if user returns form with values, get them and return to the index page
    if request.method == 'POST':
        key = str( request.form['key'] )

        #if the key is incorrect, return to incorrectkey page
        if(key != secretkey):
            return redirect(url_for('incorrectkey'))

        #if key is correct, create payload with ring times
        payload = list()
        data    = list()
        data1   = list()
        x = int(1)
        while(x<=28):
            data.append(str(request.form[str(x)]))
            x+=1
        for el in data:
            data1.append(el.split(":"))
        payload = [list( map(int,i) ) for i in data1]

        db.update({'WORK': payload}, q.type == 'worklist')
        print("Payload: ", payload)
        return redirect(url_for('index'))

#####################################################################################
#### Get the current ring times in the database, start the website on port 80
#### and start both of the threads for ringing the bell and interfacing with the lcd
#####################################################################################
if __name__=='__main__':
    #payload = db.get(q.type == 'worklist').get('WORK')
    #bell_relay_Switcher_THREAD.start()
    #lcd_interface_THREAD.start()
    app.run(host='127.0.0.1', port=8080, debug=True)

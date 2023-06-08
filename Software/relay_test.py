from gpiozero import LED
from time import sleep
print("Starting relay test, turning on and off every second, for a total of 20 seconds")

relay = LED(26)
print("relay state defined/unknown\n\n")
sleep(2)

relay.off()
print("relay OFF\n\n")
sleep(2)

i = int(0)

while(i<10):
    relay.on()
    print("relay ON\n\n")
    sleep(1)
    relay.off()
    print("relay OFF\n\n")
    sleep(1)
    i+=1
import RPi.GPIO as GPIO
import subprocess
import time

# had to follow these steps to get GPIO working on latest raspbian
# sudo apt-get remove python3-rpi.gpio
# sudo apt-get install python3-rpi-lgpio

# Define the GPIO pin you want to use
PIN = 22  # Change this to the GPIO pin number you are using

# Setup the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# living, dining, entry
lights_to_toggle = ["192.168.1.232", "192.168.1.236", "192.168.1.231"]

def toggle_callback(channel):
    # Call the bash script when the pin is toggled
    try:
        if GPIO.input(PIN) == GPIO.LOW:
            # the way the circuit is wired, if this is low it means the switch is set to "on"
            state = "true"
        else:
            state = "false"
            
        for ip in lights_to_toggle:
            subprocess.Popen(["tplink-smarthome-api", "setPowerState", ip, state])
            
        print(f'lights toggled successfully.')
    except Exception as e:
        print(f'Error executing light toggle: {e}')

# Add event detection on the GPIO pin
GPIO.add_event_detect(PIN, GPIO.BOTH, callback=toggle_callback, bouncetime=300)

print(f"Monitoring GPIO pin {PIN} for toggles. Press Ctrl+C to exit.")

try:
    # Keep the script running
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Script interrupted by user. Exiting...")
finally:
    GPIO.cleanup()

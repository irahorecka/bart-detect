# BART_detect
The Richmond BART line is 10 yards from my window, and it is loud. This is a simple python script to detect when BART is approaching my house.<br>

The setup is currently running on **Raspberry Pi 3 Model B+** using **Python 3.5**. The Pi is connected to a simple breadboard with four red LED lights. The LED lights blink in the direction of the approaching train (north or south).<br>

The approach is simple: BART has a transparent API that transmits a myriad of information. I monitor live updates of when the next train is leaving from two stations: El Cerrito Plaza and North Berkeley. Through trial and error, I deduced a latency between when the train departs and when it passes my house. In combination, this accurately triggers the LED lights to notify me of an incoming train. <br><br>

## **Python Setup**<br>
This script requires Python 3.5 and above - make sure your Raspberry Pi OS can support Python 3.5. Please look at requirements.txt for required Python libraries. Clone this repository onto your Raspberry Pi and use pip to install the necessary libraries, like this:<br><br>
```pip3 install -r requirements.txt``` <br><br>
To run the scipt, type this into the terminal of your Raspberry Pi (I have a Raspberry Pi 3B+):<br><br>
```python3 bart_detect.py```<br><br>
This script will run indefinitely until interrupted. To interrupt the script, press *CTRL + C* in your running terminal.<br><br>

## **Raspberry Pi GPIO**<br>

### How to set up your 16x2 LCD I2C display:<br>
A full tutorial: <a href=https://www.raspberrypi-spy.co.uk/2015/05/using-an-i2c-enabled-lcd-screen-with-the-raspberry-pi>How to setup your 16x2 LCD I2C display with Raspberry Pi</a><br>
A diagram of how to wire your LCD display with an I2C backpack to the Raspberry Pi:<br>
Note: The I2C backpack has an embedded PCF8574 I/O expander for the I2C bus, which allows me to connect the LCD display / I2C backpack directly to the GPIO pins on the Raspberry Pi without damaging the <a href=https://raspberrypi.stackexchange.com/questions/68172/i2c-bus-voltage>GPIO pins</a>.<br>
<p align = 'center'>
<img src=https://i.imgur.com/kSKlNOX.png alt="LCD with I2C backpack - RPi"
     width="500" height="500"><br>
</p>

### LCD demo:<br>
During downtime (i.e. when the train is not approaching), the LCD display will display the current time (Hour:Minite:Second AM/PM) and date (Month Day, Year):<br>
<p align='center'>
<img src=https://i.imgur.com/BYpenlg.jpg alt="time and date"
width="500" height="500">
</p><br>
When a train approaches, the LCD display will display:<br>
1) Where the train is approaching from:<br><br>
<p align='center'>
<img src=https://i.imgur.com/rGeWte7.jpg alt="time and date"
width="500" height="440">
</p><br>
2) The train's terminal station and number of cars:<br><br>
<p align='center'>
<img src=https://i.imgur.com/T7Kj1jh.jpg alt="time and date"
width="500" height="480">
</p><br>
<hr>

### How to set up your breadboard with LED lights:<br>
The basics: <a href="https://www.youtube.com/watch?v=BWYy3qZ315U">How to set up an LED light using your Raspberry Pi </a><br>
A slightly more elborate LED setup: <br>
<p align = 'center'>
<img src="https://projects.drogon.net/wp-content/uploads/2012/06/3led_bb3.jpg" alt="Breadboard w/ 3 LED" width="500" height="500"><br>
</p>

### LED demo:<br>
Finally, my simple LED setup:<br>
<p align = 'center'>
<img src="https://i.imgur.com/T5WDI7C.jpg" alt="4 LED setup on breadboard" width="500" height="450">
</p><br>
Please let me know if you have any questions! You are free to change BART stations to your preference, just make sure you have the correct station keys. Message me if you have any questons and we can work together to set this up!<br><br>

***Fin***

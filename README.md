# BART_detect
The Richmond BART line is 10 yards from my window, and it is loud. This is a simple python script to detect when BART is approaching my house.<br>

The setup is currently running on **Raspberry Pi 3 Model B+** using **Python 3.5**. The Pi is connected to a simple breadboard with four red LED lights. The LED lights blink in the direction of the approaching train (north or south).<br>

The approach is simple: BART has a transparent API that transmits a myriad of information. I monitor live updates of when the next train is leaving from two stations: El Cerrito Plaza and North Berkeley. Through trial and error, I deduced a latency between when the train departs and when it passes my house. In combination, this accurately triggers the LED lights to notify me of an incoming train. <br><br>

**Python Setup** <br>
This script requires Python 3.5 and above - make sure your Raspberry Pi OS can support Python 3.5. Please look at requirements.txt for required packages. Clone this repository onto your Raspberry Pi and use pip to install the necessary packages, like this:<br>
```pip3 install -r requirements.txt``` <br>
To run the scipt, type this into the terminal of your Raspberry Pi (I have a Raspberry Pi 3B+):<br>
```python3 bart_detect.py```<br>
This script will run indefinitely until interrupted, which is usually accomplished via pressing *CTRL + C* in the running terminal.<br><br>

**Raspberry Pi GPIO** <br>
How to set up your breadboard with LED lights: <br>
The basics: <a href="https://www.youtube.com/watch?v=BWYy3qZ315U">How to set up an LED light using your Raspberry Pi </a><br>
A slightly more elborate LED setup: <br>
<p align = 'center'>
<img src="https://projects.drogon.net/wp-content/uploads/2012/06/3led_bb3.jpg" alt="Breadboard w/ 3 LED" width="500" height="500"><br>
</p>
Finally, my simple LED setup:<br>
<p align = 'center'>
<img src="https://i.imgur.com/T5WDI7C.jpg" alt="4 LED setup on breadboard" width="500" height="450">
</p><br>
Please let me know if you have any questions! You are free to change BART stations to your liking. Message me if you have any questons or concerns, and we can work together to set this up!<br>

**Fin**

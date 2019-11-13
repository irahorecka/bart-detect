# BART_detect
The Richmond BART line is 10 yards from my window, and it is loud. This is a simple python script to detect when BART is approaching my house.

The setup is currently running on **Raspberry Pi 3 Model B+** using **Python 3.5**. The Pi is connected to a simple breadboard with four red LED lights. The LED lights blink in the direction of the approaching train (north or south).

The approach is simple: BART has a transparent API that transmits a myriad of information. I monitor live updates of when the next train is leaving from two stations: El Cerrito Plaza and North Berkeley. Through trial and error, I deduced a latency between when the train departs and when it passes my house. In combination, this accurately triggers the LED lights to notify me of an incoming train. 

**Raspberry Pi GPIO** <br>
How to set up your bread board with LED lights:
The basics (how to set up an LED light with your Pi): https://www.youtube.com/watch?v=BWYy3qZ315U <br>
A slightly more elborate LED setup: https://projects.drogon.net/wp-content/uploads/2012/06/3led_bb3.jpg <br>

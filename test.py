import time
import os
import visual_display as vd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Station:
    train_stations = {'nbrk': 'North Berkeley',
        'plza': 'El Cerrito Plza'
        }


def test():  # task to queue information into a manager dictionary
    while True:
        compass, station, line, no_cars = 'north', 'nbrk', 'warm springs', '10'
        station = Station.train_stations[station]
        lcd_disp = vd.LCD(station, 10)
        lcd_disp.train_detail(line, no_cars)
        
def main():
    """
    Set up queue monitoring and multiprocess environment.
    Start process when application is run.
    """
    os.chdir(BASE_DIR)
    test()


if __name__ == '__main__':
    main()

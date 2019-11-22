"""
A simple, infinitely running script to monitor, detect,
and warn the user of an incoming BART train. This is
particularly fun if you have a BART line right outside
of your room window.
"""
import datetime
import time
import multiprocessing as mp
import os
from pybart.api import BART
import timeout
import visual_display as vd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BART = BART(json_format=True)


class Station:
    """
    Store information for static data, such
    as station name.
    """
    train_stations = {'nbrk': 'North Berkeley',
                      'plza': 'El Cerrito Plaza'
                      }


class LiveFeed:
    """
    Query for live departure feed from any valid station
    """
    def __init__(self, station):
        self.station = station

    @timeout.timeout(5)  # timeout connection after 5 seconds of inactivity
    def direction_info(self):
        """
        Acquire live API information for
        specified BART stations
        """
        # body.decode('utf-8') in line 64 api.py - must decode to utf-8
        return BART.etd.etd(self.station)['station'][0]['etd']


class Scheduler:
    """
    Communicates with LiveFeed class. Sets up live feed
    queries for as many stations as desired by the user.
    """
    def __init__(self, station_list):
        self.stn_list = station_list

    def get_feed(self):
        """
        get live feed of stations in station_list
        via LiveFeed API class
        """
        return [(station, LiveFeed(station).direction_info()) for station in self.stn_list]


class Monitor:
    """
    Workhorse of the script. Query for live BART
    data, monitor time, and deploy message when
    train approaches house.
    """
    def __init__(self, direction):
        self.direction = direction
        self.temp_suspend = []
        self.time_delay = []

    def queue_sched(self, upcoming_trains):
        """
        Add schedules of trains that match stations
        inputted in main()
        """
        queue_trains = []
        for station, details in upcoming_trains:
            for item in details:
                for estimate in item['estimate']:
                    if estimate['direction'] == self.direction[station][0]:
                        queue_trains.append((station, item['destination'], estimate))
                        break
        return queue_trains

    def find_trains(self, queue_trains, real_time):
        """
        Find trains when they leave the station and
        queue them for deployment as they approach
        the house.
        """
        for station, destination, train in queue_trains:
            train_key = (train['color'], train['direction'], train['length'])
            _exit = 0
            if self.temp_suspend:
                for detail, _time in self.temp_suspend:
                    if time_comp(real_time, _time):
                        self.temp_suspend.remove((detail, _time))
                    if train_key == detail:
                        _exit = 1
            if _exit == 1:
                continue
            if train['minutes'] == 'Leaving':
                self.time_delay.append((station, destination, train['direction'],
                                        train['length'], real_time +
                                        datetime.timedelta(0, self.direction[station][1])))
                self.temp_suspend.append((train_key,
                                          real_time + datetime.timedelta(0, 120)))

    def send_to_queue(self, real_time, q):
        """
        If train is approaching the house, send
        train information to listener func to
        deploy user notification.
        """
        try:
            for sched in self.time_delay:
                if time_comp(real_time, sched[4]):
                    packet_queue = {'compass': sched[2],
                                    'station': Station.train_stations[sched[0]],
                                    'train_line': sched[1],
                                    'car_number': sched[3]
                                    }
                    q.put(packet_queue)
                    self.time_delay.remove(sched)
        except IndexError:
            pass

    def monitor_indef(self, q):
        """
        Master of the class - continuously scan
        for leaving trains from stations designated
        in main().
        """
        while True:
            try:
                t0 = time.time()
                real_time = datetime.datetime.now()
                station_list = [i for i in self.direction]
                station_list.sort()  # sort stations alphabetically
                upcoming_trains = Scheduler(station_list).get_feed()

                queue_train = self.queue_sched(upcoming_trains)
                self.find_trains(queue_train, real_time)
                self.send_to_queue(real_time, q)
            except (RuntimeError, KeyError, timeout.TimeoutError):
                time.sleep(1)
            finally:
                t1 = time.time()
                if t1 - t0 > 1:
                    pass
                else:
                    time.sleep(1 - (t1 - t0))


def time_comp(input_time, real_time):
    """
    Function to compare input time (input_time)
    to current time (real_time)
    """
    x = input_time
    y = real_time
    return (x.hour, x.minute, x.second) > (y.hour, y.minute, y.second)


def listener(q):  # task to queue information into a manager dictionary
    """
    Monitors incoming requests to trigger LED. This multiprocess
    listener is key to not disrupting the BART monitoring process.
    """
    lcd = vd.LCD()
    while True:
        packet = q.get()
        if packet == 'start':
            lcd.lcd_init()
            while True:
                try:
                    packet = q.get(False)
                except:
                    packet = None
                lcd.lcd_time()
                if isinstance(packet, dict):
                    time.sleep(0.5)
                    lcd.train_detail(packet, 6)
                    time.sleep(0.5)
                    # led_disp = vd.LED(packet)
                    # led_disp.led_lights()


def main():
    """
    Set up queue monitoring and multiprocess environment.
    Start process when application is run.
    """
    os.chdir(BASE_DIR)
    lcd = vd.LCD()
    lcd.lcd_boot()
    time.sleep(0.5)

    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(2)
    direction = {'nbrk': ['North', 85], 'plza': ['South', 140]}
    start_app = Monitor(direction)
    watcher = pool.apply_async(listener, (q,))  # first process
    job = pool.apply_async(start_app.monitor_indef, (q,))  # second multiprocess
    job.get()
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()

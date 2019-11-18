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

    def direction_info(self):
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


def monitor(direction, q):
    """
    A function to perform indefinite monitoring for upcoming
    trains. This function checks statuses of department trains
    through the BART API, and if a train is leaving, it will
    add an appropriate delay and transmit the information to
    a handler function (in my case led_trigger).
    """
    temp_suspend = []
    time_delay = []
    while True:
        try:
            tstart = time.time()
            real_time = datetime.datetime.now()
            station_list = [i for i in direction]
            station_list.sort() # sort stations alphabetically
            upcoming_trains = Scheduler(station_list).get_feed()
            queue_trains = []
            time_comp = lambda x, y: (x.hour, x.minute, x.second) > (y.hour, y.minute, y.second)
            for station, details in upcoming_trains:
                for item in details:
                    for estimate in item['estimate']:
                        if estimate['direction'] == direction[station][0]:
                            queue_trains.append((station, item['destination'], estimate))
                            break
            if temp_suspend:
                for i in temp_suspend:
                    if time_comp(real_time, i[1]):
                        temp_suspend.remove(i)

            for station, destination, train in queue_trains:
                _exit = 0
                if temp_suspend:
                    for detail, _time in temp_suspend:
                        if train == detail:
                            _exit = 1
                if _exit == 1:
                    continue
                if train['minutes'] == 'Leaving':
                    time_delay.append((station, destination, train['direction'], train['length'], real_time +
                                       datetime.timedelta(0, direction[station][1])))
                    temp_suspend.append((train, real_time + datetime.timedelta(0, 120)))
            try:
                for sched in time_delay:
                    if time_comp(real_time, sched[4]):
                        q.put((sched[2], sched[0], sched[1], sched[3]))
                        time_delay.remove(sched)
            except IndexError:
                pass
            tend = time.time()
            if 1-(tend-tstart) > 0:
                time.sleep(1-(tend-tstart))  # try to give a one second query freq, abs if < 0
        except (RuntimeError, KeyError) as error:
            print("{}. Retrying...".format(error))
            time.sleep(5)


def listener(q):  # task to queue information into a manager dictionary
    """
    Monitors incoming requests to trigger LED. This multiprocess
    listener is key to not disrupting the BART monitoring process.
    """
    while True:
        get_set = q.get()
        print(get_set)
        compass, station, line, no_cars = get_set
        station = Station.train_stations[station]
        lcd_disp = vd.LCD(station, 8)
        lcd_disp.train_detail(line, no_cars)
        # led_disp = vd.LED(compass)
        # led_disp.led_lights()


def main():
    """
    Set up queue monitoring and multiprocess environment.
    Start process when application is run.
    """
    os.chdir(BASE_DIR)
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(2)  # two processes - one for checking time, one for blinking led
    watcher = pool.apply_async(listener, (q,))  # first process
    direction = {'nbrk': ['North', 85], 'plza': ['South', 140]}
    job = pool.apply_async(monitor, (direction, q))  # second multiprocess
    job.get()
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()

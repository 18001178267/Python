import datetime
import time

import pandas as pd
import requests
import click
import threading
import queue
import tkinter as tk
# import matplotlib.animation as anime

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

real_time = '2019-08-08 08:08:08'

fake_time = '2019-07-10 13:50:05'

future_time = '2030-08-10 11:45:14'


# keep tracking all fetched data
class SensorData:
    def __init__(self, response, imei):
        response = eval(response.content) # parse http package to dict
        self.imei = imei
        self.data_dict = {}
        for i in response:
            key = datetime_to_timestamp(i['time'][:19])
            value = [float(i['sensor_1']), float(i['sensor_2']), float(i['sensor_3'])]
            self.data_dict[key] = value

    def update(self, response):
        response = eval(response.content)
        diff = datetime_to_timestamp(response[0]['time'][:19]) - self.get_times()[-1] + 10
        new_dict = {}
        for i in response[:int(diff)]:
            key = datetime_to_timestamp(i['time'][:19])
            value = [float(i['sensor_1']), float(i['sensor_2']), float(i['sensor_3'])]
            new_dict[key] = value
        self.data_dict.update(new_dict)

    def get_times(self):
        return sorted(self.data_dict)

    def get_s1(self):
        res = []
        for i in self.get_times():
            res.append(self.data_dict[i][0])
        return res

    def get_s2(self):
        res = []
        for i in self.get_times():
            res.append(self.data_dict[i][1])
        return res

    def get_s3(self):
        res = []
        for i in self.get_times():
            res.append(self.data_dict[i][2])
        return res

    def get_quartic(self):
        # return 1000 latest data as quartic list, sorted by time
        # [[time, s1, s2, s3], [time, s1, s2, s3]...]
        self.update(send_query(self.imei, future_time))
        res = []
        for i in self.get_times():
            res.append([i, self.data_dict[i][0], self.data_dict[i][1], self.data_dict[i][2]])
        return res[-1000:-1]

    def get_dict(self):
        # return dict sorted by time
        res = {}
        for i in self.get_times():
            res[i] = [self.data_dict[i][0], self.data_dict[i][1], self.data_dict[i][2]]
        return res


def send_query(imei, end_time):
    """
    :param imei: string as 15-digits number
    :param end_time: string in datetime format '%Y-%m-%d %H:%M:%S'
    :return: Response object
    """
    r1 = requests.get(url='http://115.29.209.155:8080/TFSV1_sensor/vehicle.ak?',
                      params={
                          'method': 'get_sensor_data',
                          'imei': imei,
                          'endTime': end_time})
    return r1


def datetime_to_timestamp(dt):
    """
    :param dt: string in datetime format '%Y-%m-%d %H:%M:%S'
    :return: float as timestamp in seconds
    """
    return time.mktime(datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S').timetuple())


def timestamp_to_datetime(ts):
    """
    :param ts: float as seconds for time stamp
    :return: string as datetime
    """
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


@click.group()
def cli():
    """
    A little sensor monitor tool that show/fetch data of sensor you selected by IMEI.

    Note: please use quotation marks wrap the datetime in arguments

    Examples:

    monitor fetch '2019-08-08 08:00:00' '2019-08-08 08:08:08' 1145141919810

    monitor watch 1145141919810

    """
    ...
    pass


@click.command()
@click.argument('start')
@click.argument('end')
@click.argument('imei')
def fetch(start, end, imei):
    # fetch data in user pointed interval
    real_imei_2 = imei
    s2 = int(datetime_to_timestamp(start))
    e2 = int(datetime_to_timestamp(end))
    sd = SensorData(send_query(real_imei_2, start), real_imei_2)
    for i in range(s2, e2, 90):
        sd.update(send_query(real_imei_2, timestamp_to_datetime(i)))
        click.echo('fetch #' + str(i) + ' done')
    to_save = pd.DataFrame.from_dict(sd.get_dict())
    fn = timestamp_to_datetime(sd.get_times()[0]) + ' to ' + timestamp_to_datetime(sd.get_times()[-1]) + '.csv'
    fn = fn.replace(':', '_').replace(' ', '_')
    to_save.to_csv(fn)


@click.command()
@click.argument('imei')
def watch(imei):
    # real-time monitor mode
    real_imei_2 = imei
    
    # initialize gui window and drawing area
    root = tk.Tk()
    root.wm_title("sensor info monitor")

    fig = Figure(figsize=(10, 6), dpi=100)
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    
    # start record data
    start_time = time.time()
    sd = SensorData(send_query(real_imei_2, future_time), real_imei_2)
    notify_queue = queue.Queue()
    x_ts = sd.get_times()
    # time convert
    x_sec = [int(t % 3600) for t in x_ts]
    if 0 in x_sec:
        num_h = x_ts[0] // 3600
        x_sec = [(t - (num_h * 3600)) for t in x_ts]
    y_s1 = sd.get_s1()
    y_s2 = sd.get_s2()
    y_s3 = sd.get_s3()

    # initialize drawing
    l1, = ax1.plot(x_sec, y_s1)
    l2, = ax2.plot(x_sec, y_s2)
    l3, = ax3.plot(x_sec, y_s3)
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def on_closing():
        # call when close the window
        end_time = time.time()
        fetch(start_time, end_time, sd.imei)
        root.quit()
        root.destroy()

    def on_key_press(event):
        # click.echo("you pressed {}".format(event.key))
        key_press_handler(event, canvas, toolbar)

    def _quit():
        # call when press quit button
        on_closing()
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def refresh_figure(frame):
        # refresh data every second and renew graph
        ax1.clear()
        ax2.clear()
        ax3.clear()
        x_ts = [f[0] for f in frame]
        x_sec = [int(t % 3600) for t in x_ts]
        # time convert
        if 0 in x_sec:
            num_h = x_ts[0] // 3600
            x_sec = [(t - (num_h * 3600)) for t in x_ts]
        y_s1 = [f[1] for f in frame]
        y_s2 = [f[2] for f in frame]
        y_s3 = [f[3] for f in frame]
        l1.set_data(x_sec, y_s1)
        l2.set_data(x_sec, y_s2)
        l3.set_data(x_sec, y_s3)
        ax1.plot(x_sec, y_s1)
        ax2.plot(x_sec, y_s2)
        ax3.plot(x_sec, y_s3)
        canvas.draw()
        return l1, l2, l3

    def query_data():
        yield sd.get_quartic()

    def process_msg():
        # message queue for data acquiring process
        root.after(400, process_msg)
        while not notify_queue.empty():
            # print("check queue")
            try:
                msg = notify_queue.get()
                if msg[0] == 1:
                    refresh_figure(msg[1])

            except queue.Empty:
                pass

    def execute_asyn():
        # data acquiring process
        def scan(_queue):
            while True:
                r = sd.get_quartic()
                _queue.put((1, r))

        th = threading.Thread(target=scan, args=(notify_queue,))
        th.setDaemon(True)
        th.start()

    canvas.mpl_connect("key_press_event", on_key_press)
    button = tk.Button(master=root, text="quit", command=_quit)
    button.pack(side=tk.BOTTOM)
    
    # kick start everything
    # ani = anime.FuncAnimation(fig, refresh_figure, frames=query_data, interval=25)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    process_msg()
    execute_asyn()
    tk.mainloop()
    return 0


# register command for cli
cli.add_command(watch)
cli.add_command(fetch)


if __name__ == '__main__':
    cli()

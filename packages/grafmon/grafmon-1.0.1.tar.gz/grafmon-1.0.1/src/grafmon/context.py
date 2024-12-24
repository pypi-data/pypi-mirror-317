import argparse
import os
import sys
import time

from enum import Enum

class MonitorType(Enum):
    BUILTIN = 1
    USER = 2

class Context:
    def __init__(self,
                 monitor_cmd: str | None = None,
                 refresh_rate: int = 1000,
                 max_ticks: int = 60):
        self.monitor_cmd = monitor_cmd
        self.refresh_rate = refresh_rate
        self.max_ticks = max_ticks
        self.tick_index = -1
        self.tick_time = None
        self.tick_mod = 5
        self.monitor_type = MonitorType.BUILTIN
        self.selected_width = 4

    def initFromFile(self, path: str):
        pass

    def initFromArgs(self, args: list[str] | None = None):
        parser = argparse.ArgumentParser(description='Monitor metrics in a real-time time-series graph');

        group = parser.add_mutually_exclusive_group()
        group.add_argument('-m', '--monitor',
                            type = str,
                            default = 'pcpu',
                            help = 'Select from builtin monitors to feed data into monitor [default: pcpu]')
        group.add_argument('-c', '--command',
                            type = str,
                            default = None,
                            help = 'User command to feed data into monitor [example: ps -eo rss,pid,comm --no-headers]')

        parser.add_argument('-r', '--refreshrate',
                            type = int,
                            default = 1000,
                            help='Refresh rate in milliseconds [default: 1000]')
        parser.add_argument('-t', '--ticks',
                            type = int,
                            default = 60,
                            help='Count of ticks on X axis [default: 60]')
        parser.add_argument('-l', '--labels',
                            type = int,
                            default = 10,
                            help='Count of labels on X axis [default: 10]')
        parser.add_argument('--list-monitors',
                            action = 'store_true',
                            default = False,
                            help = 'List available builtin monitors')

        if args == None:
            args = parser.parse_args()
        else:
            args = parser.parse_args(args)

        if args.list_monitors:
            self.list_monitors()
            sys.exit(0)

        if args.command == None:
            monitor = os.path.join(os.path.dirname(__file__), 'monitors', args.monitor)
            if not os.path.exists(monitor):
                print(f"No such builtin monitor `{args.monitor}`. Use `--list-monitors` to list available builtin monitors.")
                sys.exit(1)
            self.monitor_cmd = monitor
        else:
            self.monitor_cmd = args.command
            self.monitor_type = MonitorType.USER

        self.refresh_rate = args.refreshrate
        self.max_ticks = args.ticks

        labels = args.labels
        if labels > self.max_ticks:
            labels = self.max_ticks
        self.tick_mod = self.max_ticks // args.labels
        if self.tick_mod == 0:
            self.tick_mod = 1

    def update_tick(self):
        self.tick_index += 1;
        if self.tick_index == self.max_ticks:
            self.tick_index = 0
        self.tick_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
        self.mainwindow.rgn.setRegion((self.tick_index, self.tick_index))

    def list_monitors(self):
        print("Builtin monitors:")
        data_path = os.path.join(os.path.dirname(__file__), 'monitors')
        for monitor in sorted(os.listdir(data_path)):
            with open(os.path.join(data_path, monitor), 'r') as f:
                lines = f.readlines()
                lines[1] = lines[1][2:].rstrip()
                print(f"{monitor:10} {lines[1]}")

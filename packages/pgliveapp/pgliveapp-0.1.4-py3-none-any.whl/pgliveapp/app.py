import pickle
import queue
import signal
import socket
from threading import Thread
from typing import Any, List, Optional

import numpy as np
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LiveAxisRange, LivePlotWidget
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow


class LivePlotApp(QApplication):
    def __init__(
        self,
        *,
        num: int = 1,
        plot_titles: List = [],
        cols: int = 1,
        argv: List[str] = [],
        **kwargs,
    ):
        super().__init__(argv)

        _xrange = kwargs.get("xrange", None)
        if not _xrange is None:
            _xrange = LiveAxisRange(fixed_range=[-_xrange, _xrange])
        _yrange = kwargs.get("yrange", None)
        if not _yrange is None:
            _yrange = LiveAxisRange(fixed_range=[-_yrange, _yrange])

        self.connectors = {}
        self.data_queue = queue.Queue(maxsize=5)

        self.SOCK_ADDRESS = (
            kwargs.get("ip", "localhost"),
            kwargs.get("port", 4000),
        )
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.sock.bind(self.SOCK_ADDRESS)

        self.main_window = QMainWindow()
        self.main_window.setStyleSheet(
            """
            QMainWindow {
                background-color: black;
            }
            """
        )
        self.panel = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(parent=self.panel)

        for ch in range(num):
            plot_title = (
                plot_titles[ch]
                if ch < len(plot_titles)
                else f"Live Plot {ch + 1}"
            )
            rows = (num + cols - 1) // cols
            plot_row = ch % rows
            plot_col = ch // rows
            plot_widget = LinePlotWidget(
                plot_key=f"y{ch+1}",
                x_range_controller=_xrange,
                y_range_controller=_yrange,
                x_points=kwargs.get("x_points", 5000),
                title=plot_title,
            )
            self.layout.addWidget(
                plot_widget,
                plot_row,
                plot_col,
            )
            self.connectors[plot_widget.plot_key] = plot_widget.connector

        self.server_timer = QtCore.QTimer()
        self.server_timer.timeout.connect(self.live_plot)
        self.server_timer.start(10)

        Thread(target=self.live_plot, daemon=True).start()

        self.main_window.setCentralWidget(self.panel)
        self.main_window.show()

        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)

        self.exec()

    def live_plot(self):
        try:
            mes, addr = self.sock.recvfrom(1024 * 10)
            if not mes:
                return
        except:
            return False

        data = pickle.loads(mes)
        x = data["x"]
        for key, connector in self.connectors.items():
            y = data[key]
            if isinstance(y, list):
                _step = len(y)
                connector.cb_append_data_array(
                    y, np.arange(x * _step, x * _step + _step)
                )
            else:
                connector.cb_append_data_point(y, x)

    def handle_exit(self, signum, frame):
        print("Exiting...")
        self.quit()


class LinePlotWidget(LivePlotWidget):
    def __init__(
        self,
        plot_key: str,
        parent=None,
        background: str = "default",
        plotItem=None,
        x_range_controller: Optional[LiveAxisRange] = None,
        y_range_controller: Optional[LiveAxisRange] = None,
        x_points: int = 5000,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            parent,
            background,
            plotItem,
            x_range_controller,
            y_range_controller,
            **kwargs,
        )
        self.plot_key = plot_key
        self.curve = LiveLinePlot(pen=kwargs.get("pen", "r"))
        self.addItem(self.curve)
        self.connector = DataConnector(
            self.curve, max_points=x_points, update_rate=200
        )


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--num", type=int, default=1)
    parser.add_argument("--cols", type=int, default=1)
    parser.add_argument("--port", type=int, default=4000)
    parser.add_argument("--ip", type=str, default="localhost")
    parser.add_argument("--xrange", type=float, default=None)
    parser.add_argument("--yrange", type=float, default=None)
    parser.add_argument("--x-points", type=int, default=5000)
    args = parser.parse_args()

    LivePlotApp(**vars(args))

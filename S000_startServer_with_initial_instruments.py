import os
import argparse
import logging

from qcodes.tests.instrument_mocks import DummyInstrument

from instrumentserver import QtWidgets, QtCore
from instrumentserver.log import setupLogging, log, LogLevels
from instrumentserver.server import startServer
from instrumentserver.server.application import startServerGuiApplication
# from S001_initial_instruments import initial_Instruments


setupLogging(addStreamHandler=True,
             logFile=os.path.abspath('instrumentserver.log'))
logger = logging.getLogger('instrumentserver')
logger.setLevel(logging.DEBUG)


def server(port=5555, user_shutdown=False, instruments={}):
    app = QtCore.QCoreApplication([])
    server_, thread = startServer(port, user_shutdown)
    initialize_station(server_.station, instruments)
    thread.finished.connect(app.quit)
    return app.exec_(), server_


def serverWithGui(port=5555, instruments={}):
    app = QtWidgets.QApplication([])
    window = startServerGuiApplication(port)
    station = window.stationServer.station
    initialize_station(station, instruments)
    return app.exec_()

def initialize_station(station, instruments={}):
    for inst_name, inst_info in instruments.items():
        driver_cls = inst_info["driver_class"]
        inst_info.pop("driver_class")
        inst = driver_cls(inst_name, **inst_info)
        station.add_component(inst)

def script() -> None:
    parser = argparse.ArgumentParser(description='Starting the instrumentserver')
    parser.add_argument("--port", default=5555)
    parser.add_argument("--gui", default=True)
    parser.add_argument("--allow_user_shutdown", default=False)
    args = parser.parse_args()

    if args.gui:
        serverWithGui(args.port)
    else:
        app_exec, server_ = server(args.port, args.allow_user_shutdown)

if __name__ == "__main__":
    script()



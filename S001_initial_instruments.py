from S000_startServer_with_initial_instruments import serverWithGui, server

from Hatlab_QCoDes_Drivers.SignalCore_SC5511A import SignalCore_SC5511A
from Hatlab_QCoDes_Drivers.SignalCore_sc5506a_seperate import SignalCore_SC5506A
from Hatlab_QCoDes_Drivers.Keysight_N5183B import Keysight_N5183B
from Hatlab_QCoDes_Drivers.Keysight_N9020A import Keysight_N9020A
from Hatlab_QCoDes_Drivers.MiniCircuits_SwitchMatrix_Multi import MiniCircuits_SwitchMatrix_Multi
from Hatlab_QCoDes_Drivers.Yokogawa_GS200_USB import Yokogawa_GS200_USB
from switch_control_20201224 import modes as switch_modes

initial_Instruments ={
    "MXA": {"driver_class": Keysight_N9020A, "address": 'TCPIP0::169.254.180.116::INSTR'},

    "SWT": {"driver_class": MiniCircuits_SwitchMatrix_Multi, "name_list": ["SWT1", "SWT2", "SWT3"],
            "address_list": ['http://169.254.254.251', 'http://169.254.254.249', 'http://169.254.254.252'],
            "mode_dict": switch_modes},

    # "YOKO": {"driver_class": Yokogawa_GS200_USB, "serial_number": '91UA31819'},

    "SC_Q1": {"driver_class": SignalCore_SC5506A,  "serial_number": "100024DF", "channel": 1},
    "SC_C1": {"driver_class": SignalCore_SC5511A,  "serial_number": "10001C4C"},
    "SC_C1_50": {"driver_class": SignalCore_SC5511A,  "serial_number": "1000190F"},
    "SC_Q1_CSB": {"driver_class": SignalCore_SC5506A,  "serial_number": "100024DF", "channel": 2},

    "SC_Q2": {"driver_class": SignalCore_SC5506A, "serial_number": "100024DE", "channel": 2},
    "SC_C2": {"driver_class": SignalCore_SC5511A, "serial_number": "100024E0"},
    "SC_C2_50": {"driver_class": SignalCore_SC5511A, "serial_number": "1000156A"},
    "SC_C2_CSB": {"driver_class": SignalCore_SC5511A, "serial_number": "10000E9D"},

    "SC_Q3": {"driver_class": SignalCore_SC5506A, "serial_number": "10001A85", "channel": 1},
    "SC_C3": {"driver_class": Keysight_N5183B, "address": 'TCPIP0::169.254.253.232::inst0::INSTR'},
    "SC_C3_50": {"driver_class": SignalCore_SC5511A, "serial_number": "10001C4F"},
    "SC_C3_CSB": {"driver_class": SignalCore_SC5511A, "serial_number": "10001850"},

    "SC_SNAIL_1": {"driver_class": SignalCore_SC5506A, "serial_number": "100024DE", "channel": 1},
    "SC_SNAIL_2": {"driver_class": SignalCore_SC5506A, "serial_number": "10001A85", "channel": 2},
}

if __name__ == "__main__":
    serverWithGui(instruments=initial_Instruments)
    # server(instruments=initial_Instruments)
#!/usr/bin/env python3

"""
A class to represent a user that has been detected on a network.
"""

from time import perf_counter
from typing import Tuple
from postgresql_timestamp import timestamp

__author__ = 'Nick Dawson'
__copyright__ = 'Copyright 2020, RITSEC'
__license__ = 'MIT'
__version__ = '0.1.0'
__status__ = 'Development'


class NetworkUser:
    """
    A class to represent a user that has been detected on a network.
    """
    def __init__(self, mac_address: str, signal_strength: float):
        """
        Initialize the user and store the start time to later compute the
        total time the user was visible.
        :param str mac_address: MAC Address ex. '00:0a:95:9d:68:16'
        :param float signal_strength: represent network signal strength ex. -70.653
        """
        self.start_time = timestamp()
        self.mac_address = mac_address.lower()
        self.signal_strengths = []
        self.signal_strengths.append(signal_strength)

    def update(self, signal_strength: float) -> None:
        """
        Add another signal strength data point to the list.
        :param float signal_strength: float to represent network signal strength ex. -70.653
        """
        self.signal_strengths.append(signal_strength)

    def done(self) -> Tuple[str, str, float, float, float, float, float, float]:
        """
        Run calculations to compute total time visible on the network and,
        the average signal strength.
        :return: Tuple in the format of:
            (MAC address, total time, average signal strength, min signal strength, max signal strength)
        """
        end_time = timestamp()
        avg_signal_strength = sum(self.signal_strengths) / len(self.signal_strengths)
        return (timestamp(),
                self.mac_address,
                self.start_time,
                end_time,
                avg_signal_strength,
                min(self.signal_strengths),
                max(self.signal_strengths)
                )

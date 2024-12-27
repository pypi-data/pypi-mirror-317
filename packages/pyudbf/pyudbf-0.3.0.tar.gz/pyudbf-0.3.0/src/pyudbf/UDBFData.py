import numpy as np
from dataclasses import dataclass
from typing import List, Any
from datetime import datetime


@dataclass(frozen=True)
class UDBFHeader:
    """Data-class for meta-data of the UDBFData class.

    Attributes:
        udbf_version (int): Version of the UDBF file structure times 100.
        vendor (str): Vendor id in the UDBF data.
        sampling_rate (float): Sampling rate of the data in Hz.
        channel_names (list[str]): List of names of the channels.
        channel_directions (list[int]): IO direction of the channel
                            (0 -> input, 1 -> output, 2 -> IO, 3 -> empty).
        channel_types (list[int]): Datatype of channel.
                                   E.g. 1 -> Boolean or 8 -> float.
        channel_precision (list[int]): Precision of channel.
        number_of_channels (int): Number of channels in the data.
    """

    udbf_version: int
    vendor: str
    sampling_rate: float
    channel_names: List[str]
    channel_directions: List[int]
    channel_types: List[int]
    channel_units: List[str]
    channel_precision: List[int]

    def name(self, channel: int) -> str:
        """Name of the channel

        Args: channel (int): Index of channel in channel-list
        """

        return self.channel_names[channel]

    def unit(self, channel: int) -> str:
        """Unit of the data in the channel

        Args: channel (int): Index of channel in channel-list
        """

        return self.channel_units[channel]

    @property
    def number_of_channels(self):
        return len(self.channel_units)


@dataclass(frozen=True)
class UDBFData:
    """Data-class for data read as UDBF.
    This class holds channel data as well as the UDBF
    header and is the main class to operate with.

    Attributes:
        timestamps (list[datetime]): List of timestamps
                                     for the channel data.
        _signals (list[list[np.any]]): Each element is a list
                                       wich contains the raw data
                                       for all channels as a list
                                       at the timestamp corresponding
                                       to the index.
        channel_signals (list[list[np.any]): Each element is a list
                                             corresponding to one channel
                                             which contains the raw data
                                             list of the channel
                                             for all timstamps.
        n_points (int): Number of data points in each channel.
        n_channels (int): Number of channels.
        runlength (float): Time between first and last
                           datum of the channel data in seconds.
        header (UDBFHeader): Header for the data.
    """

    timestamps: List[datetime]
    _signals: List[List[Any]]
    header: UDBFHeader

    @property
    def channel_signals(self):
        return np.transpose(self._signals)

    @property
    def n_points(self):
        return len(self.timestamps)

    @property
    def n_channels(self):
        return self.header.number_of_channels

    @property
    def runlength(self):
        delta = self.timestamps[-1] - self.timestamps[0]
        return delta.total_seconds()

    def serialize_to_ascii(self, outfile):
        """Serialize all data to ASCII.

        Args:
            outfile (str): Name of the output file. Appends to file when
                           the file already exists.
        """

        amplitude_array = []

        channels = [c for c in range(self.n_channels)]

        for channel in channels:
            signal = self.signal(channel)
            amplitude_array.append(signal)

        with open(outfile, "a+") as fout:
            first_line = "Sampling frequency: "
            first_line += str(self.header.sampling_rate) + "\n"

            fout.write(first_line)
            line = ""
            for i in channels:
                line += str(self.header.name(i).replace(" ", "_"))
                line += " "
            line += "\n"
            fout.write(line)

            n_events = len(amplitude_array[0])

            for i in range(n_events):
                line = ""
                for k in range(len(amplitude_array)):
                    line += str(amplitude_array[k][i])
                    line += " "
                line += "\n"
                fout.write(line)

    def signal(self, channel: int) -> list:
        """List of data in the given channel corresponding to self.timestamps.

        Args:
            channel (int): Channel id.
        """
        return self.channel_signals[channel]

    def channel(self, name: str) -> list:
        """List of data in the given channel corresponding to self.timestamps.

        Args:
            name (str): Channel name
        """
        return self.channel_signals[self.header.channel_names.index(name)]

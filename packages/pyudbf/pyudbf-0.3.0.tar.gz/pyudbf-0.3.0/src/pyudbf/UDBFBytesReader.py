from pyudbf.UDBFParser import UDBFParser, BytesReader
from pyudbf.UDBFData import UDBFData


class UDBFBytesReader(UDBFData):
    """Class used to read UDBF data given as bytestring.
    """

    def __init__(self, udbf_data: bytes):
        """
        Args:
            udbf_data: Input UDBF data.
        """

        reader = BytesReader(udbf_data)
        parser = UDBFParser(reader)

        timestamps, signals = parser.signal()
        header = parser.header

        super().__init__(timestamps, signals, header)

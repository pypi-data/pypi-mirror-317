from pyudbf.UDBFParser import UDBFParser, BytesReader
from pyudbf.UDBFData import UDBFData


class UDBFFileReader(UDBFData):
    """Class used to read an UDBF file given as filename.
    """

    def __init__(self, infile: str):
        """
        Args:
            infile: Input UDBF filename
        """

        self.infile = infile
        with open(infile, mode="rb") as fin:
            data = fin.read()

        reader = BytesReader(data)
        parser = UDBFParser(reader)

        timestamps, signals = parser.signal()
        header = parser.header

        super().__init__(timestamps, signals, header)

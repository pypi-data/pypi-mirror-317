# pyudbf
## General
A python implementation of the UDBF ("Universal Data Bin File") data format version 1.07. The UDBF format is e.g. frequently used for data exchange with 
Gantner Instruments data acquisition systems.

## Installation via pip
```
pip install pyudbf
```

## Examples
The "tests"-folder in the projects github repository contains a small example UDBF file called example.udbf. In the following, it is assumed that this file is located at "./tests/example.udbf".

### Simple file reader
```
python tests/udbf_file_reader.py --help
python tests/udbf_file_reader.py --in tests/example.udbf
```

## Example for usage in own projects
The following python code provides an entry point for the usage of pyudbf in own projects.

```
from pyudbf import UDBFFileReader
# get access to the file
udbf_data = UDBFFileReader('./tests/example.udbf')

# show all information of data file header
print(udbf_data.header.__dict__)
print('Channel count: ' + str(udbf_data.n_channels))
print('Data point count: ' + str(udbf_data.n_points))
print('Data record: ' + str(udbf_data.runlength) + ' s')

# show all existing channels
print(udbf_data.header.channel_names)

# get data of specific channels
timestamp = udbf_data.timestamps
camera_links_X = udbf_data.signal(7)  # get values of selected channel by index
camera_links_X = udbf_data.channel('camera links X')  # get values of selected channel by name
```

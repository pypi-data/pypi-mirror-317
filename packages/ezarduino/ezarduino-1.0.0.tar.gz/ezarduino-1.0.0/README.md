# ezarduino
![Static Badge](https://img.shields.io/badge/3.12.1-blue?style=for-the-badge&logo=python&logoColor=white&label=python)
![Static Badge](https://img.shields.io/badge/3.5-green?style=for-the-badge&logo=python&logoColor=white&label=pyserial)

`ezarduino` is a Python library designed to facilitate communication between Python and Arduino devices via the Arduino Serial Port (ASP). It provides a Python-based reconstruction of Arduino's Serial class, making it easier to send and receive data between your Python scripts and Arduino projects.

## Features

- Easy-to-use class for managing Arduino devices over serial ports.
- Core functionality mirroring Arduino's `Serial` class.
- Support for:
  - Reading bytes and strings from Arduino.
  - Writing data to Arduino.
  - Checking available bytes and write readiness.
- Built-in support for encoding (default: UTF-8).

## Installation

To install `ezarduino` from the PyPi, run the next command:
```bash
pip install ezarduino
```

But to install `ezarduino` from the repo, run the next commands:
```bash
git clone https://github.com/cr4t3/ezarduino.git
cd ezarduino
pip install .
```

## Usage

Here is a quick example to demonstrate the basic functionality of `ezarduino`:

### Example: Sending and Receiving Data

```python
from ezarduino import ArduinoDevice

# Connect to Arduino (adjust COM por, baud rate and timeout as necessary)
arduino = ArduinoDevice(com="COM3", baud_rate=9600, timeout=1000)

# Send data to Arduino
arduino.println("Hello, Arduino!")

# Read data from Arduino
try:
    while arduino.available():
        print("Received:", arduino.readString())
except IndexError:
    print("No data available to read.")

# Close connection
arduino.end()
```

## API Reference

### `ArduinoDevice`

#### Initialization

```python
ArduinoDevice(com: str, baud_rate: int = 9600, timeout: int = 1000, encoding: str = "utf-8")
```

- **com**: Serial port of the Arduino device (e.g., `"COM3"` or `"/dev/ttyUSB0"`).
- **baud_rate**: Communication speed (default: `9600`).
- **timeout**: Timeout in milliseconds (default: `1000`).
- **encoding**: Encoding used for string communication (default: `UTF-8`).

#### Methods

- **`available()`**: Returns the number of bytes available for reading.
- **`availableForWriting()`**: Returns the number of bytes available for writing.
- **`end()`**: Closes the serial port connection.
- **`begin()`**: Initializes the serial port connection.
- **`find(target: str, length: int = 0)`**: Searches for a character in the serial buffer.
- **`findUntil(target: str, terminal: str)`**: Searches for a character in the serial buffer until a terminal character is found.
- **`flush()`**: Waits until all data is written to the serial port.
- **`parseFloat(lookahead: LookaheadMode = SKIP_ALL, ignore: strs = None)`**: Reads a float from the serial buffer.
- **`parseInt(lookahead: LookaheadMode = SKIP_ALL, ignore: str = None)`**: Reads an integer from the serial buffer.
- **`read()`**: Reads one byte from the serial buffer.
- **`readBytes(buffer: list[byte], length: int)`**: Reads a specified number of bytes into a buffer.
- **`readBytesUntil(character: str, buffer: list[str or byte], length: int)`**: Reads bytes into a buffer until a specified character is found.
- **`readString()`**: Reads all available bytes from the serial buffer as a string.
- **`readStringUntil(terminator: str)`**: Reads bytes from the serial buffer until a terminator character is found.
- **`print(val: any, format: FormatMode = None)`**: Prints a value to the serial buffer.
- **`println(val: any, format: FormatMode = None)`**: Prints a value to the serial buffer followed by a newline.
- **`setTimeout(time: int)`**: Sets the timeout for the serial port connection.
- **`write(val) OR write(str) OR write(buf, len)`**: Writes data to the serial buffer.

## Contributing

We welcome contributions! If you would like to contribute to `ezarduino`, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

For issues, suggestions, or feedback, please open a GitHub Issue in the repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Requirements

- Python 3.12.1 or newer
- pyserial 3.5 or newer

## Acknowledgments
Special thanks to the open-source community for inspiring this project. Let's make Arduino projects even more accessible with Python!
import serial
import time
from .errors import _TypeError, _NotEnoughError, _MoreThanExpectedArgsError
import string

byte = bytes
char = str

def ischar(x: any) -> bool:    
    if isinstance(x, str) and len(x) == 1:
        return True
    
    return False

def isbyte(x: any) -> bool:
    if isinstance(x, bytes) and len(x) == 1:
        return True
    
    return False

LookaheadMode = int
FormatMode = int

class ArduinoDevice:
    # Formats
    DEC = 0
    HEX = 1
    OCT = 2
    BIN = 3

    # Lookahead modes
    SKIP_ALL = 4
    SKIP_NONE = 5
    SKIP_WHITESPACE = 6

    def __init__(self, com: str, baud_rate: int = 9600, timeout: int = 1000, encoding: str = "utf-8") -> None:
        """Initalize the Arduino Serial Port (ASP) connection.

        Args:
            com (str): Port name or location to which the Arduino is connected.
            baud_rate (int, optional): The baud rate which the Arduino is set. Defaults to 9600.
            timeout (int, optional): Timeout rate in milliseconds. Defaults to 1000.
            encoding (str, optional): Encoding used to send information. Defaults to "utf-8".

        Raises:
            _TypeError: If any argument is not the expected type.
        """        
        if not isinstance(com, str):
            raise _TypeError("com", "str")
        
        if not isinstance(baud_rate, int):
            raise _TypeError("baud_rate", "int")
        
        if not isinstance(timeout, int):
            raise _TypeError("timeout", "int")
        
        if not isinstance(encoding, str):
            raise _TypeError("encoding", "str")

        self.__com = com
        self.__baud_rate = baud_rate
        self.__timeout = timeout
        self.__encoding = encoding
        self.__ready = False
        self.begin()
    
    def available(self) -> int:
        """Returns the amount of available bytes to read.

        Returns:
            int: Amount of available bytes to read
        """        
        if not self.__ready:
            return 0
        return self.device.in_waiting
    
    def availableForWriting(self) -> int:
        """Returns the amount of available bytes to write

        Returns:
            int: Amount of available bytes to write
        """        
        if not self.__ready:
            return 0
        return self.device.out_waiting

    def end(self) -> None:
        """Closes the ASP connection"""        
        self.device.close()
        self.__ready = False
        return
    
    def begin(self) -> None:
        """Initializes a connection by the Arduino Serial Port (ASP). Called on __init__ method of this class."""        
        self.__ready = False
        self.device = serial.Serial(self.__com, self.__baud_rate, timeout=self.__timeout/1000)
        time.sleep(2)
        self.__ready = True

    def find(self, target: char, length: int = 0) -> bool:
        """Finds a character on the ASP.

        Args:
            target (char): Searched char.
            length (int, optional): Max length of readabilty of the ASP buffer. Defaults to 0 (for no limit).

        Raises:
            _TypeError: In case that target is not a char or length is not an int

        Returns:
            bool: Returns the 'found' state of the character.
        """        
        if not ischar(target):
            raise _TypeError("target", "char (one-length string)")
        
        if not isinstance(length, int):
            raise _TypeError("length", "int")

        target_byte = target.encode()

        while self.available():
            if self.read() == target_byte:
                return True
            
            if length and self.available() <= length:
                break

        return False
    
    def findUntil(self, target: char, terminal: char) -> bool:
        """Finds a character on the ASP if is not before the terminal char.

        Args:
            target (char): Character to search on the ASP buffer.
            terminal (char): Character that ends the search (if target not found) on the ASP buffer.

        Raises:
            _TypeError: If target or terminal aren't a char.

        Returns:
            bool: True if target was found before a terminal char or EOF. Returns False otherwise.
        """        
        if not ischar(target):
            raise _TypeError("target", "char (one-length string)")
        
        if not ischar(terminal):
            raise _TypeError("terminal", "char (one-length string)")

        target_byte = target.encode()
        terminal_byte = terminal.encode()

        while self.available():
            current_byte = self.read()
            if current_byte == target_byte:
                return True

            if current_byte == terminal_byte:
                break

        return False

    def flush(self) -> None:
        """Waits until all data is written."""
        self.device.flush()
        
    def parseFloat(self, lookahead: LookaheadMode = SKIP_ALL, ignore: char | None = None) -> float:
        """Reads a float from the ASP buffer.

        Args:
            lookahead (LookaheadMode, optional): Lookahead mode. Defaults to SKIP_ALL.
            ignore (char | None, optional): Character to ignore. Defaults to None.

        Raises:
            _TypeError: If lookahead is not a LookaheadMode or ignore is not a char or None.

        Returns:
            float: Read float.
        """        
        if not isinstance(lookahead, LookaheadMode) or self.SKIP_ALL <= lookahead <= self.SKIP_WHITESPACE:
            raise _TypeError("lookahead", "LookaheadMode")

        if not ischar(ignore) and ignore != None:
            raise _TypeError("ignore", "char (one-length string) or None")

        buffer = []
        readable = list(string.digits + ".-")

        def __char_readable(char: char, buffer: list) -> None:
            buffer.append(char)
            if char == ".":
                readable.remove(".")
            elif char == "-" and len(buffer) > 1:
                readable.remove("-")

        while self.available():
            current_char = self.read().decode(self.__encoding)
            if current_char in readable:
                __char_readable(current_char, buffer)
            elif current_char == ignore:
                continue
            else:
                match lookahead:
                    case self.SKIP_ALL:
                        continue
                    case self.SKIP_NONE:
                        break
                    case self.SKIP_WHITESPACE:
                        if current_char.isspace():
                            continue
                        else:
                            break
        if (
            not buffer or
            buffer.count(".") > 1 or
            buffer.count("-") > 1 or
            not any(c.isdigit() for c in buffer if c not in [".", "-"])
        ): return 0.0
        else: return float("".join(buffer))
    
    def parseInt(self, lookahead: LookaheadMode = SKIP_ALL, ignore: char | None = None) -> int:
        """Reads an integer from the ASP buffer.

        Args:
            lookahead (LookaheadMode, optional): Lookahead mode. Defaults to SKIP_ALL.
            ignore (char | None, optional): Character to ignore. Defaults to None.

        Raises:
            _TypeError: If lookahead is not a LookaheadMode or ignore is not a char or None.

        Returns:
            int: Read integer.
        """        
        if not isinstance(lookahead, LookaheadMode) or self.SKIP_ALL <= lookahead <= self.SKIP_WHITESPACE:
            raise _TypeError("lookahead", "LookaheadMode")

        if not ischar(ignore) and ignore != None:
            raise _TypeError("ignore", "char (one-length string) or None")

        buffer = []
        readable = list(string.digits + "-")

        def __char_readable(char: char, buffer: list) -> None:
            buffer.append(char)
            if char == "-" and len(buffer) > 1:
                readable.remove("-")

        while self.available():
            current_char = self.read().decode(self.__encoding)
            if current_char in readable:
                __char_readable(current_char, buffer)
            elif current_char == ignore:
                continue
            else:
                match lookahead:
                    case self.SKIP_ALL:
                        continue
                    case self.SKIP_NONE:
                        break
                    case self.SKIP_WHITESPACE:
                        if current_char.isspace():
                            continue
                        else:
                            break
        if (
            not buffer or
            buffer.count("-") > 1 or
            not any(c.isdigit() for c in buffer if c != "-")
        ): return 0
        else: return int("".join(buffer))

    def read(self) -> byte:
        """Reads one byte from the ASP buffer

        Raises:
            _NotEnoughError: If there isn't an available byte to read

        Returns:
            byte: Read byte.
        """
        if not self.available():
            raise _NotEnoughError("bytes")

        return self.device.read(1)
    
    def readBytes(self, buffer: list[byte], length: int) -> int:
        """Reads a 'length'-length bytes into buffer

        Args:
            buffer (list[byte]): Buffer which we have bytes appended.
            length (int): Amount of bytes to read

        Raises:
            _TypeError: If buffer is not a list[byte] or length is not int
            _NotEnoughError: If length is more than available bytes.

        Returns:
            int: Amount of bytes read
        """
        if not isinstance(buffer, list) or not all([isbyte(_) for _ in buffer]):
            raise _TypeError("buffer", "list[byte]")
        
        if not isinstance(length, int):
            raise _TypeError("length", "int")
        
        start_len = len(buffer)

        if not self.available():
            raise _NotEnoughError("bytes")

        for _ in range(length):
            if not self.available():
                raise _NotEnoughError("bytes")
            
            buffer.append(self.device.read(1))
        return len(buffer) - start_len

    def readBytesUntil(self, character: char, buffer: list[char | byte], length: int) -> int | None:
        """Reads bytes until it founds the 'character' on the ASP buffer.

        Args:
            character (char): Character to terminate.
            buffer (list[char  |  byte]): Array of char or bytes used as buffer.
            length (int): Max length to read.

        Raises:
            _TypeError: If character is not a char, buffer is not a list[char | byte], or length is not a int

        Returns:
            int: Amount of bytes read to buffer.
            None: If character wasn't found.
        """        
        if not isinstance(character, char) or len(character) != 1:
            raise _TypeError("character", "char (one-length string)")

        if not isinstance(buffer, list) or not (all([ischar(_) for _ in buffer]) or all([isbyte(_) for _ in buffer])):
            raise _TypeError("buffer", "list[char] or list[byte]")

        if not isinstance(length, int):
            raise _TypeError("length", "int")
        
        if length <= 0:
            return 0

        start_len = len(buffer)

        while self.available()-length:
            read_byte = self.read().decode(self.__encoding)
            buffer.append(read_byte)
            
            if read_byte == character:
                return start_len-len(buffer)
        else:
            return None
    
    def readString(self) -> str:
        """Reads all available bytes from the ASP buffer as a string.

        Raises:
            _NotEnoughError: If there isn't any available byte to read.

        Returns:
            str: All the bytes read as a string.
        """        
        if self.available == 0:
            raise _NotEnoughError("text")
        
        return self.device.readall().decode(self.__encoding)
    
    def readStringUntil(self, terminator: char) -> str | None:
        """Reads all available bytes from the ASP buffer until the terminator char.

        Args:
            terminator (char): Char which ends the reading.

        Raises:
            _TypeError: If terminator is not a char.

        Returns:
            str: All the bytes read until the terminator char.
            None: If the terminator char wasn't found.
        """        
        if not isinstance(terminator, char) or len(terminator) != 1:
            raise _TypeError("terminator", "char (one-length string)")

        buffer = []
        while self.available():
            read_byte = self.read().decode(self.__encoding)
            buffer.append(read_byte)
            
            if read_byte == terminator:
                return "".join(buffer)
        else:
            return None
    
    def print(self, val: any, format: FormatMode | None = None) -> int:
        """Prints a value to the ASP buffer.

        Args:
            val (any): Value to print.
            format (FormatMode, optional): Format to print the value. Optional.

        Raises:
            _TypeError: If format is not a FormatMode or None.

        Returns:
            int: Length of the printed value.
        """        
        if not (isinstance(format, FormatMode) or None) or (isinstance(format, FormatMode) and not self.DEC <= format <= self.BIN):
            raise _TypeError("format", "FormatMode or None")
        
        if format:
            match format:
                case self.DEC:
                    val = int(val)
                case self.HEX:
                    val = hex(int(val))
                case self.OCT:
                    val = oct(int(val))
                case self.BIN:
                    val = bin(int(val))
        
        self.device.write(str(val).encode(self.__encoding))
        return len(val)

    def println(self, val: any, format: FormatMode | None = None) -> int:
        """Prints a value to the ASP buffer and adds a newline character.

        Args:
            val (any): Value to print.
            format (str, optional): Format to print the value. Optional.

        Raises:
            _TypeError: If format is not a FormatMode or None.

        Returns:
            int: Length of the printed value.
        """        
        if not (isinstance(format, FormatMode) or None) or (isinstance(format, FormatMode) and not self.DEC <= format <= self.BIN):
            raise _TypeError("format", "FormatMode or None")

        val = val + "\r\n"
        self.print(val, format = format)
        return len(val)
    
    def setTimeout(self, time: int) -> None:
        """Sets the timeout of the ASP connection.

        Args:
            time (int): Timeout in milliseconds.

        Raises:
            _TypeError: If time is not an int.
        """        
        if not isinstance(time, int):
            raise _TypeError("time", "int")
        
        self.device.timeout = time / 1000

    def write(self, *args) -> int:
        """Writes a value to the ASP buffer.

        Raises:
            _MoreThanExpectedArgsError: If the amount of arguments is more than 2.
            _TypeError: If the value is not an int or str. If the buffer is not a list[char | byte]. If the length is not an int.
            _NotEnoughError: If the buffer is not enough to write.

        Returns:
            int: Length of the written value.
        """        
        if len(args) == 0 or len(args) > 2:
            raise _MoreThanExpectedArgsError("write", 2, len(args))
        
        if len(args) == 1:
            if isinstance(args[0], int) and 0 <= args[0] <= 255:
                val = args[0]
                self.device.write(val)
                return 1
            elif isinstance(args[0], str):
                str_ = args[0]
                bytes_str = str_.encode(self.__encoding)
                self.device.write(bytes_str)
                return len(bytes_str)
            else:
                raise _TypeError("val", "int or str")
        else:
            buf: list[char | byte] = args[0]
            len_: int = args[1]
            if not isinstance(buf, (list, str)) or (isinstance(buf, list) and not (all(ischar(_) for _ in buf) or all(isinstance(_, int) and 0 <= _ <= 255 for _ in buf))):
                raise _TypeError("buf", "list[char | byte]")
            
            if not isinstance(len_, int):
                raise _TypeError("len", "int")
            
            if len_ > len(buf):
                raise _NotEnoughError("elements")
            
            if all([ischar(_) for _ in buf]):
                str_buf = "".join(buf)
                self.device.write(str_buf.encode(self.__encoding))
                return len(str_buf)
            else:
                bytes_buf = bytes(buf)
                self.device.write(bytes_buf)
                return len(bytes_buf)

    def __bool__(self) -> bool:
        return self.__ready
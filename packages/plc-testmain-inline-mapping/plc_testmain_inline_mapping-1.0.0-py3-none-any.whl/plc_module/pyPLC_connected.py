import serial
import asyncio
import serial_asyncio
        
class SerialProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self._is_connected = False
        self._response = ""
 
    def connection_made(self, transport):
        self.transport = transport
        self._is_connected = True
        print(f"Connection established to serial port")
 
    def data_received(self, data):
        """Handles the data received from the PLC, ensuring it's formatted like the sent command."""
        self._response += data.decode('utf-8').strip()
        print(f"Data received: {self._response}")
 
    def connection_lost(self, exc):
        print("Connection lost")
        asyncio.get_event_loop().stop()
        self._is_connected = False
 
    def get_response(self):
        response = self._response
        self._response = ""
        return response
 
class PLCConnection:
    def __init__(self, port, baudrate=9600, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self._transport = None
        self._protocol = None
 
    async def initialize_connection(self):
        """Initialize the serial connection asynchronously."""
        loop = asyncio.get_running_loop()
        self._protocol = SerialProtocol()
        try:
            self._transport, _ = await serial_asyncio.create_serial_connection(
                loop, lambda: self._protocol, self.port, baudrate=self.baudrate,
                parity=self.parity, stopbits=self.stopbits, bytesize=self.bytesize
            )
 
            print("Serial connection established.")
 
        except serial.SerialException as e:
            print(f"Failed to initialize serial connection: {e}")
        except Exception as e:
            print(f"Unexpected error during connection initialization: {e}")
 
    async def read_plc(self, read_address, read_data):
        """
        Sends a read command to the PLC and returns the response.
        """
        if len(read_address) != 4 or (read_data and len(read_data) != 4):
            print("Error: Read address and length must be 4 characters long")
            return
 
        read_string = f"@00RD{read_address}{read_data}"
 
        Q = 0
        for char in read_string:
            Q ^= ord(char)
        read_string += f"{Q:X}*\r"  
 
        self._transport.write(read_string.encode("utf-8"))
        print(f"Sending read command: {read_string}")
 
        await asyncio.sleep(0.5)
 
        response = self._protocol.get_response()
        if not response:
            print("*** Incomplete response received during read ***")
            return None
        print(f"Response after read: {response}")
        read_data = response[7:len(response)-3] 
        return response
 
    async def write_plc(self, write_address, write_data):
        """Sends a write command to the PLC."""
        if len(write_address) != 4 or len(write_data) != 4:
            print("Error: Write address and data must be 4 characters long")
            return
 
        write_string = f"@00WD{write_address}{write_data}"
 
        Q = 0
        for char in write_string:
            Q ^= ord(char)
        write_string += f"{Q:X}*\r"  
 
        print(f"Sending write command: {write_string}")
 
        self._transport.write(write_string.encode("utf-8"))
 
    async def set_auto_mode(self):
        """Sets the PLC handler into Auto Mode and verifies if the mode is set."""
        write_address = "3000"
        write_data = "0002"
 
        print("Sending Auto Mode to Handler")
        await self.write_plc(write_address, write_data)
 
        await asyncio.sleep(1)
 
        self._protocol._response = ""
        read_address = "4002"
        read_data = "0001"
        response = await self.read_plc(read_address, read_data)
 
        if not response:
            print("Error: Failed to read Auto Mode status from the handler.")
            return
 
        if "0002" in response:
            print("\nAuto Mode Received ...")
        
        elif "0003" in response:
            print("Initialization done auto mode")

        else:
            print("\n*** Auto Mode Not Received, Check if Production Page ***")
            await self.set_stop_mode()
 
    async def set_stop_mode(self):
        """Sets the PLC handler into STOP mode and handles error conditions like the Visual Basic code."""
        write_address = "3000"
        write_data = "0000"
 
        print("Sending STOP Mode to Handler")
        await self.write_plc(write_address, write_data)
 
        # Simulate timeout and read response
        timeout = 1
        await asyncio.sleep(timeout)
 
        dummy_response = ""
        try:
            dummy_response = self._protocol.get_response()
        except asyncio.TimeoutError:
            print("Error while reading data from PLC after write command")
 
        if not dummy_response or len(dummy_response) < 10:
            print(f"Old Dummy response: '{dummy_response}'")
            print("Attempting to read again...")
            try:
                dummy_response = self._protocol.get_response()
            except asyncio.TimeoutError:
                print("Error while reading data from PLC a second time")
 
            print(f"New Dummy response: '{dummy_response}'")

    async def move_presser_to_retrieve_pos(self):
        await self.write_plc("4012", "0012")
        await asyncio.sleep(1)
        self._protocol._response = ""
        response = await self.read_plc("4512", "0001")
        if "4512" in response:
            print("Presser shifted to retrieve position")

    async def move_presser_to_long_probe_pos(self):
        await self.write_plc("4005", "0005")
        await asyncio.sleep(1)
        self._protocol._response = ""
        response = await self.read_plc("4508", "0001")
        if "0008" in response:
            print("Presser shifted to long probe position")

    async def move_presser_to_all_probe_pos(self):
        await self.write_plc("4007", "0007")
        await asyncio.sleep(1)
        self._protocol._response = ""
        response = await self.read_plc("3051", "0001")
        if "0130" in response:
            print("Presser shifted to all probe position")

    async def move_presser_to_retest_pos(self):
        await self.write_plc("4009", "0009")
        await asyncio.sleep(1)
        self._protocol._response = ""
        response = await self.read_plc("4510", "0001")
        if "4510" in response:
            print("Presser shifted to retest position")

    async def get_plc_version(self):
        response = await self.read_plc("1636", "0003") # <- read 3 address in one go
        await asyncio.sleep(1)
        resp = response[7:len(response)-3] 
        plc_rev = ""
        for i in range(0, len(resp), 2):
            byte = int(resp[i:i+2], 16)
            plc_rev += chr(byte)
        print(f"PLC Revision: {plc_rev}")

    async def get_jig_id(self):   # not sure if need read 3900 or 1620 
        read_data = "0001"
        response = await self.read_plc("3900", read_data)
        return response[7:11]
    
    async def get_conveyor_width(self):  # this function does not give conveyor width
        response = await self.read_plc("1622", "0001")
        resp_conveyor = response[7:11]
        conveyor_width = ""
        for i in range(0, len(resp_conveyor), 2):
            byte = int(resp_conveyor[i:i+2], 16)
            conveyor_width += str(byte)
        return conveyor_width
 
    async def close_connection(self):
        """Closes the serial connection."""
        if self._transport:
            self._transport.close()
            self._protocol._is_connected = False
            print("Connection closed.")
 
async def main():
    plc_connection = PLCConnection("COM4")
    await plc_connection.initialize_connection()

    print(await plc_connection.get_conveyor_width())

    #print(await plc_connection.get_plc_version())

    #print(await plc_connection.get_jig_id())
 
    #await plc_connection.set_auto_mode()
 
    #await plc_connection.set_stop_mode()

    #await plc_connection.move_presser_to_retest_pos()

    #await plc_connection.read_plc("1600", "0004")
 
    await plc_connection.close_connection()
 
# Start the asyncio event loop and run main
asyncio.run(main())

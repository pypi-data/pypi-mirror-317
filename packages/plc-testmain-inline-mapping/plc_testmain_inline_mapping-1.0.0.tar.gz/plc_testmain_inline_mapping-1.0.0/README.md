# pyPLC_connected

# installments

1. py -m pip install notebook (run on cmd prompt)
2. run jupyter notebook - py -m notebook (run on cmd prompt)
3. py -m pip install plc_testmain_inline_mapping

# using pyPLC_connected.py

on jupyter notebook
1. from plc_module import pyPLC_connected
2. import asyncio

# How to run functions
3. async def main():
    4. plc = pyPLC_connected.PLCConnection(COM port number)

    5. await plc.initialize_connection()

    6. await plc.function_name(input)

    7. await plc.close_connection()

8. asyncio.run(main())

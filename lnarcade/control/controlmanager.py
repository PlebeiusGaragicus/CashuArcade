import os
import platform
import time
import logging
logger = logging.getLogger()

class ControlManager():
    def __init__(self):
        self.setup_correctly = False

        # check if on MacOS
        # NOTE: now done in lnarcade/app.py
        # if platform.system() == 'Darwin':
        #     logger.critical("ControlManager::__init__() -> ControlManager not supported on MacOS")
        #     return

        if os.getenv( "BLINKA_FT232H", None ) is None:
            logger.critical("ControlManager::__init__() -> BLINKA_FT232H not set")
            return

        try:
            import board
            from adafruit_seesaw import seesaw, rotaryio, digitalio
        except ImportError:
            logger.critical("ControlManager::__init__() -> ImportError")
            return

        self.i2c = board.I2C()
        self.seesaw = seesaw.Seesaw(self.i2c, 0x36)

        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
        self.seesaw.pin_mode(24, self.seesaw.INPUT_PULLUP)
        self.switch = digitalio.DigitalIO(self.seesaw, 24)

        # Get current volume from the system
        volume_query = os.popen("amixer get 'Master' | grep -m1 -o [0-9]*% | tr -d %").read().strip()
        self.current_volume = int(volume_query)

        self.setup_correctly = True


    def run(self):
        if not self.setup_correctly:
            logger.critical("ControlManager::run() returning -> not setup correctly")
            return
        else:
            logger.info("running control manager run()")
        # return


        
        last_position = -1
        while True:
            position = -self.encoder.position

            if position != last_position:
                # print(position)

                if position > last_position:
                    self.current_volume = min(100, self.current_volume + 5)  # increase by 5%

                else:
                    self.current_volume = max(0, self.current_volume - 5)  # decrease by 5%

                # Adjust system volume using the 'amixer' command
                v = f"amixer set 'Master' -- {self.current_volume}%"
                os.system(v)

            last_position = position

            # time.sleep(10)
            time.sleep(0.1)




TODO = """
https://www.youtube.com/watch?v=Rt5xtIyxgco

https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/linux

https://learn.adafruit.com/custom-hid-devices-in-circuitpython

https://learn.adafruit.com/adafruit-i2c-qt-rotary-encoder/python-circuitpython

https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-mcp2221/post-install-checks


"""

# import hid
# device = hid.device()
# device.open(0x04D8, 0x00DD)
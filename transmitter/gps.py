"""
gps.py
Tristan Van Cise
GPS class for retrieving coords from ultimate GPS v3
03/19/2020

Device: 
    * Ultimate GPS Breakout V3
"""

import time
import board
import busio
import adafruit_gps

class GPS:
    def __init__(self):
        # Use default RPI 3 Model B TX/RX GPIO pins
        RX_PIN = board.RX # GPIO 15
        TX_PIN = board.TX # GPIO 14
        
        self.uart = busio.UART(TX_PIN, RX_PIN, baudrate=9600, timeout=600)
        self.gps = adafruit_gps.GPS(self.uart)
        self.init_gps()

    def init_gps(self):
        """
            According to: https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

            FORMAT: bit [NAME], // Description
            0 NMEA_SEN_GLL, // GPGLL interval - Geographic Position - Latitude longitude 
            1 NMEA_SEN_RMC, // GPRMC interval - Recommended Minimum Specific GNSS Sentence 
            2 NMEA_SEN_VTG, // GPVTG interval - Course over Ground and Ground Speed 
            3 NMEA_SEN_GGA, // GPGGA interval - GPS Fix Data 
            4 NMEA_SEN_GSA, // GPGSA interval - GNSS DOPS and Active Satellites 
            5 NMEA_SEN_GSV, // GPGSV interval - GNSS Satellites in View
        """
        # Set NMEA sentence output frequencies 
        # Turn on RMC & GGA
        self.gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

        # Set NMEA port update rate
        # <once every 1000ms>
        self.gps.send_command(b'PMTK220,1000')

    # Used as a replacement of sleep to avoid using a blocking call
    # to wait to process gps.update() data every [wait_time]ms
    def wait_time_elapsed(self,wait_time):
        self.current_time = time.monotonic()
        has_elapsed = self.current_time - self.last_time >= wait_time
        if has_elapsed:
            self.last_time = time.monotonic()
        return has_elapsed

    # Start GPS data loop
    def track(self):
        self.last_time = time.monotonic()
        while True:
            # Must be called every loop iteration to ensure all data is read
            self.gps.update()
            if self.wait_time_elapsed(1.0):
                if not self.gps.has_fix:
                    # No fix.. Wait for fix
                    print("GPS has not established position data. Waiting for fix...")
                    continue

                # GPS has a fix and is ready to report data
                print("Latitude: {}".format(self.gps.latitude))
                print("Longitude: {}".format(self.gps.longitude))
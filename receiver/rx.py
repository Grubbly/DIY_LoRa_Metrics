"""
rx.py
Tristan Van Cise
Receiver code for stationary LoRa device at my house
Adapted from Brent Rubell's code @ Adafruit Industries
03/19/2020

Devices: 
    * RFM9X LoRa Radio
    * 128x32 I2C OLED Display
"""

import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

text_split_size = 15

while True:
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('Tristan LoRa', 35, 0, 1)

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        display.show()
        display.text('-  ME WANT DATA  -\n-    NOM  NOM    -', 15, 15, 1)
    else:
        # Display the packet text and rssi
        display.fill(0)
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        
        display.text('RX: ', 0, 0, 1)
        packet_len = len(packet_text)
        if packet_len > text_split_size:
            for char_counter in range(0, packet_len, text_split_size):
                start_index = char_counter
                end_index = char_counter+text_split_size - packet_len
                display.text(packet_text[start_index:end_index], 25, 8*((char_counter) // text_split_size), 1)
            
            start_index = packet_len-(packet_len%text_split_size)
            if start_index == packet_len:
                start_index -= text_split_size
            display.text(packet_text[start_index:], 25, 8 * ((packet_len//text_split_size)), 1)
        else:
            display.text(packet_text, 25, 0, 1)

        print("RECEIVED: {}".format(packet_text))

    display.show()

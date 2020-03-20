import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x
from gps import GPS

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Setup OLED
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

# Clear display
display.fill(0)
display.show()

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
lora_radio = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
lora_radio.tx_power = 23

display_change = True

def set_header_text():
    display.text('Tristan Van Cise', 19, 0, 1)
    display.text('- LoRa Transmitter -', 8, 10, 1)

def set_display(text):
    display.fill(0)
    set_header_text()
    display.text(text, 8, 24, 1)
    display.show()

def send_gps(gps):
    data = bytes("{:.6f},{:.6f}".format(gps.latitude, gps.longitude), encoding='utf8')
    lora_radio.send(data)

def display_gps(gps):
    display_text = "{:.6f},{:.6f}".format(gps.latitude, gps.longitude)
    set_display(display_text)

def setup_lora_radio():
    CS = DigitalInOut(board.CE1)
    RESET = DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    lora_radio = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    lora_radio.tx_power = 23

def init():
    set_header_text()
    display.show()

if __name__ == "__main__":
    init()
    gps = GPS()
    try:
        while True:
            try:
                for gps_instance in gps.track():
                    print("="*50)
                    print("Latitude: {0:.6f} degrees".format(gps_instance.latitude))
                    print("Longitude: {0:.6f} degrees".format(gps_instance.longitude))
                    print("Fix quality: {}".format(gps_instance.fix_quality))
                    if gps_instance.satellites is not None:
                        print("# satellites: {}".format(gps_instance.satellites))
                    if gps_instance.altitude_m is not None:
                        print("Altitude: {} meters".format(gps_instance.altitude_m))
                    if gps_instance.speed_knots is not None:
                        print("Speed: {} knots".format(gps_instance.speed_knots))
                    if gps_instance.track_angle_deg is not None:
                        print("Track angle: {} degrees".format(gps_instance.track_angle_deg))
                    print("="*50 + "\n")

                    display_gps(gps_instance)
                    send_gps(gps_instance)

            except RuntimeError as e:
                print("Runtime error occured... continuing transmit loop:")
                print("Exception message: ", e)
                # Radio object dies on signal timeout
                # so reinitialize to make everything work again
                setup_lora_radio()
                continue
    except KeyboardInterrupt:
        print("Keyboard interrupt detected!")
        print("Terminating transmitter program...")

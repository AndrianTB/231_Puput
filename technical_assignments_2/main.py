import time
from gpiozero import MCP3008, DistanceSensor
from ubidots import ApiClient

# Konfigurasi MCP3008
adc = MCP3008(channel=0, max_voltage=3.3)

# Konfigurasi Sensor Ultrasonik
ultrasonic_sensor = DistanceSensor(echo=24, trigger=23)

# Konfigurasi Ubidots
API_KEY = "BBFF-5dac962870a6d5d2a5f32eb06da46f8676d"
VARIABLE_VOLTAGE = "64d44fdeab3ca3000c1a85d5"
VARIABLE_DISTANCE = "64d7336afbda9b000dda1472"

api = ApiClient(API_KEY)
variable_voltage = api.get_variable(VARIABLE_VOLTAGE)
variable_distance = api.get_variable(VARIABLE_DISTANCE)

def read_voltage():
    raw_value = adc.value
    voltage = raw_value * 3.3  # 3.3V reference voltage
    voltage_divided = voltage * 5  # 5x voltage divider
    return voltage_divided

while True:
    try:
        voltage = read_voltage()
        print("Voltage:", voltage)
        
        distance = ultrasonic_sensor.distance * 100  # Convert to centimeters
        print("Distance:", distance)
        
        # Kirim data ke Ubidots
        variable_voltage.save_value({"value": voltage})
        variable_distance.save_value({"value": distance})
        
        time.sleep(1)  # Kirim data setiap 10 detik
        
    except KeyboardInterrupt:
        break

print("Program selesai.")

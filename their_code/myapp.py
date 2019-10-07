#def application(environ, start_response):
#    status = '200 OK'
#    output = get_current_numbers()

#    response_headers = [('Content-type', 'text/plain'),
#                        ('Content-Length', str(len(output)))]
#    start_response(status, response_headers)

#    return [output]
import serial
#ser = serial.Serial('/dev/ttyS0', 115200)
ser = serial.Serial('/dev/ttyUSB0', 115200)

def get_current_numbers():
    """get the current data from the serial port 0 and return it as a normalized pair"""
    
    return normalize_numbers(ser.readline())


def normalize_numbers(raw_numbers):
    """normalize numbers"""
    parts = raw_numbers.split()
    print("raw numbers: {0}".format(raw_numbers))
    #print("sensor 1: {0}".format(parts[0]))
    #print("sensor 2: {0}".format(parts[1]))      
    sensor1 = normalize_sensor_1(parts[0])
    sensor2 = normalize_sensor_2(parts[1])
    return "{:3d},{:3d}".format(int(sensor1),int(sensor2))

def normalize(curr,min,max,mult):
    return ((curr - min)/(max - min))*mult

def cap(curr):
    if curr > 100:
        return 100
    elif curr < 0:
        return 0
    else:
        return curr

def normalize_sensor_1(sensor1string):
    """980 (100) to 175 (0)"""
    just_the_number1 = sensor1string[3:]
    number1 = int(just_the_number1)
    return cap(100-normalize(number1,175,980,100))
    

def normalize_sensor_2(sensor2string):
    """135 (100) to 230 (0)"""
    just_the_number2 = sensor2string[3:]
    number2 = int(just_the_number2)
    return cap(100-normalize(number2,135,230,100))

def save_to_web(numbers):
    """ save to numbers/index.html """
    f = open("/var/www/html/numbers/index.html","w",encoding="utf8")
    f.write(numbers)
    f.close()
    
while True:
    try:
        current_numbers = get_current_numbers()
        print(current_numbers)
        save_to_web(current_numbers)
    except Exception as e:
        print(e)

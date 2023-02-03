from pyModbusTCP.client import ModbusClient
import datetime
import time
import requests
import schedule

machine_info = {
    'GDC_7': {
        'type':'GDC_7',
        'ip': ' 192.168.3.19',
        'start_reg': 1,
        'reg_length': 34,
        'pName': ['Good_Count', 'Bad_Count'],

        'access_token': ""
    },
    'GDC_8': {
        'type': 'GDC_8',
        'ip': ' 192.168.3.19',
            'start_reg': 1,
            'reg_length': 34,
            'pName': ['Good_Count', 'Bad_Count'],

            'access_token': ""
        },
    'GDC_9': {
        'type': 'GDC_9',
        'ip': ' 192.168.3.19',
            'start_reg': 1,
            'reg_length': 34,
            'pName': ['Good_Count', 'Bad_Count'],

            'access_token': ""
        },
    'GDC_10': {
        'type': 'GDC_10',
        'ip': ' 192.168.3.19',
            'start_reg': 1,
            'reg_length': 34,
            'pName':['Good_Count', 'Bad_Count'],

            'access_token': ""
        }
}
HOST = "10.13.4.39:8080"
#  Every -- Seconds send data to server
sample_rate = 5
# To Stop sending data to server
send_data = True
headers = {"Content-Type": 'application/json'}


def Values():
    """The Main function to handle other calls"""
    global headers
    for m_name, m_info in machine_info.items():
        data = getValues(m_info['ip'], m_info['start_reg'],
                         m_info['reg_length'])

        try:
            if data is None:
                post_mb_error(m_name, m_info['access_token'])
            else:
                postValues(data, m_name, m_info['access_token'], m_info['pName'])
        except Exception as e:
            print(e)


schedule.every(sample_rate).seconds.do(Values)


def getValues(ip, start, length):
    """For initializing the modbus tcp client and reading data from it"""
    mb_client = initiate_client(ip)
    data = readValues(mb_client, ip, start, length)
    return data


def initiate_client(ip):
    """returns the modbus client instance"""
    print('Modbus Client IP: ', ip)
    return ModbusClient(host=ip, port=502, unit_id=1, auto_open=True, auto_close=True, timeout=2)


def readValues(mb_client, ip, start, length):
    """reads poke yoke values from the client"""
    try:
        if type=='GDC_7':
            try:
                data1 = mb_client.read_holding_registers(5004, 1)
                data2 = mb_client.read_holding_registers(5604, 1)
                register_data = data1 + data2
                print(f"got values {register_data}")
                return register_data
            except Exception as e:
                print(datetime.datetime.now(), "Error in reading Client", ip, e, end=" ")
        elif type == 'GDC_8':
             try:

                data1 = mb_client.read_holding_registers(5001, 1)
                data2 = mb_client.read_holding_registers(5601, 1)
                register_data = data1 + data2
                print(f"got values {register_data}")
                return register_data
             except Exception as e:
                print(datetime.datetime.now(), "Error in reading Client", ip, e, end=" ")
        elif type == 'GDC_9':
            try:
                data1 = mb_client.read_holding_registers(5002,1)
                data2 = mb_client.read_holding_registers(5601,1)
                register_data = data1 + data2
                print(f"got values {register_data}")
                return register_data
            except Exception as e:
                print(datetime.datetime.now(), "Error in reading Client", ip, e, end=" ")
        elif type == 'GDC_10':
            try:
                data1 = mb_client.read_holding_registers(5003, 1)
                data2 = mb_client.read_holding_registers(5603, 1)
                register_data = data1 + data2
                print(f"got values {register_data}")
                return register_data
            except Exception as e:
                print(datetime.datetime.now(), "Error in reading Client", ip, e, end=" ")

        return None


def post_mb_error(m_name, accessToken):
    """posting an error in the attributes if the data is None"""
    global headers
    url = f'http://{HOST}/api/v1/{accessToken}/attributes'
    payload = {'machine': m_name, "error": True}
    print(str(payload))

    if send_data:
        request_response = requests.post(url, json=payload, headers=headers, timeout=2)
        print(request_response.text)


def postValues(data, m_name, accessToken, parameterName):
    """posting poke yoke telemetry values to HIS Cloud app"""
    global headers
    # print(data)
    url = f'http://{HOST}/api/v1/{accessToken}/telemetry'

    payload = {'machine': m_name}

    for i, pName in enumerate(parameterName):
        payload[pName] = data[i]
    print(str(payload))

    if send_data:
        request_response = requests.post(url, json=payload, headers=headers, timeout=2)
        print(request_response.text)


while True:
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        break

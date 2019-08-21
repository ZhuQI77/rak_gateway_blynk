import rak_db
from rak_loraserver import rak_loraserver
import json
import base64

TOPIC = "application/#"


rak_node_test = rak_db.rak_db()

global_curent_dev_eui = ''
global_dev_index = ''



import blynklib

VPIN_GET_NODE_LISTBUTTEN = 70
VPIN_NODE_LIST_MENU = 71
VPIN_DATA_INFO_TERMINAL = 72
VPIN_GAUGE_TEMPERATURE = 73
VPIN_GAUGE_HUMIDITY = 74
VPIN_VALUE_DISPLAY = 75

BLYNK_AUTH = 'TqFnlK7E6m3IfVfyLNGeDDsP4QOGI0hb'
blynk = blynklib.Blynk(BLYNK_AUTH)
rak_node_test = rak_db.rak_db()

def blynk_send_invalid():
    blynk_send_last_humidity('--')
    blynk_send_last_temperature('--')
    blynk_send_last_seen('--')

def blynk_send_str_to_terminal(str_data):
    print('send to terminal:%s' % str_data)
    blynk.virtual_write(VPIN_DATA_INFO_TERMINAL, str_data)

def blynk_send_one_data_to_terminal(data_info):
    str_data = '[%s]\n  humidity:%.2f﹪RH\n  temperature:%.2f°C\n' % (data_info[0], data_info[1] * 0.5, data_info[2] * 0.1)
    blynk_send_str_to_terminal(str_data)

def blynk_send_last_seen(date_time):
    blynk.virtual_write(VPIN_VALUE_DISPLAY, date_time)

def blynk_send_last_temperature(temperature):
    if isinstance(temperature, int):
        str_temperature = '%.2f' % (int(temperature) * 0.1)
    elif isinstance(temperature, str):
        str_temperature = '--'
    else:
        str_temperature = '--'
    print('[blynk_send_last_temperature] %s' % str_temperature)
    blynk.virtual_write(VPIN_GAUGE_TEMPERATURE, str_temperature)

def blynk_send_last_humidity(humidity):
    if isinstance(humidity, int):
        str_humidity = '%.2f' % (int(humidity) * 0.5)
    elif isinstance(humidity, str):
        str_humidity = '--'
    else:
        str_humidity = '--'
    print('[blynk_send_last_humidity] %s' % str_humidity)
    blynk.virtual_write(VPIN_GAUGE_HUMIDITY, str_humidity)

def blynk_send_dev_data_to_terminal(dev_index):
    print('[blynk_send_dev_data_to_terminal]')
    try:
        data_tuple = rak_node_test.select_node_data(dev_index)
        dev_str = rak_node_test.get_node_dev(dev_index)
        global global_curent_dev_eui
        global_curent_dev_eui = dev_str;
        global global_dev_index
        global_dev_index = dev_index
        if len(data_tuple) == 0:
            str = '%s\'s log is empty.\n' % dev_str
            blynk_send_str_to_terminal(str)
            blynk_send_invalid()
        else:
            print('van 004: len data_tuple:%d' % len(data_tuple))
            str = '\n%s\n' % dev_str
            blynk_send_str_to_terminal(str)
            blynk_send_last_seen(data_tuple[0][0])
            blynk_send_last_humidity(data_tuple[0][1])
            blynk_send_last_temperature(data_tuple[0][2])
            for data_info in data_tuple:
                blynk_send_one_data_to_terminal(data_info)

    except Exception as e:
        raise e
        print(e)
    finally:
        pass


@blynk.handle_event('write V71')
def read_virtual_pin_handler(pin, value):
    print('menu')
    print(value[0])

    try:
        dev_index = int(value[0]) - 1
        node_tuple = rak_node_test.get_nodes()
        blynk.set_property(VPIN_NODE_LIST_MENU, 'labels', *node_tuple)
        if dev_index > len(node_tuple):
            blynk_send_invalid()
            blynk_send_str_to_terminal('Error! Please press \'GET NODE\' button first.\n')
            print('dev_index:%d, max_index:%d' % (dev_index, len(node_tuple)))
        else:
            blynk_send_dev_data_to_terminal(dev_index)

    except Exception as e:
        print('Exception _1')
        print(e)
        blynk_send_str_to_terminal(e)
    finally:
        pass


@blynk.handle_event('write V70')
def write_virtual_pin_handler(pin, value):
    print('444444')
#    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if int(value[0]) == 0:
        print('444444 return')
        return
    try:
        node_tuple = rak_node_test.get_nodes()
        blynk.set_property(VPIN_NODE_LIST_MENU, 'labels', *node_tuple)
        blynk_send_invalid()
        blynk_send_str_to_terminal('Get node list success!\n')
    except Exception as e:
        print('Exception _2')
        print(e)
    finally:
        pass

class insert_db_a(rak_loraserver):
    def __init__(self, server_ip='127.0.0.1', server_port=1883):
        super().__init__(server_ip, server_port)
        pass

    def on_message_come(self, client, userdata, msg):
        print('on_message_come')
        data_info = []
        #    print('[on_message_come] in')
        #    print(str(msg.payload))
        str_lora_rx = str(msg.payload, 'utf-8')
        #    print(str_lora_rx)
        #    print("************************************88")
        str_lora_rx = str_lora_rx.lstrip('b')
        str_lora_rx = str_lora_rx.lstrip('\'')
        str_lora_rx = str_lora_rx.rstrip('\'')
        print(msg.topic + " " + ":" + str_lora_rx)

        #    print('[on_message_come] in 001')
        try:
            json_rx = json.loads(str_lora_rx)
        except Exception as e:
            print('[on_message_come] in json.loads error')
            print(str_lora_rx)
            print(e)
        finally:
            pass

        app_name = json_rx['applicationName']
        dev_eui = json_rx['devEUI']
        data_info.append(dev_eui)
        if ('data' in json_rx):
            rx_data = base64.b64decode(json_rx['data'])
        else:
            return None

        # gps,加头共11byte，不关注，去除抛弃
        if ((0x01 == rx_data[0]) and (0x88 == rx_data[1])):
            #            print('[on_message_come] gps')
            rx_data = rx_data[11:]

        # battery，加头共4byte
        if ((0x08 == rx_data[0]) and (0x02 == rx_data[1])):
            int_voltage = int.from_bytes(rx_data[2:4], byteorder='big', signed=True)  ##signed标志是否为有符号数
            float_voltage = int_voltage * 0.01
            rx_data = rx_data[4:]

        # Acceleration，加头共8byte，不关注，抛弃
        if ((0x03 == rx_data[0]) and (0x71 == rx_data[1])):
            rx_data = rx_data[8:]

        # humidity,湿度，加头共3byte
        if ((0x07 == rx_data[0]) and (0x68 == rx_data[1])):
            #            print('[on_message_come] humidity')
            try:
                int_humidity = int.from_bytes(rx_data[2:3], byteorder='big', signed=True)
            except Exception as e:
                print('humidity error')
                print(e)
            finally:
                pass

            rx_data = rx_data[3:]

        # pressure,加头共4byte
        if ((0x06 == rx_data[0]) and (0x73 == rx_data[1])):
            int_pressure = int.from_bytes(rx_data[2:4], byteorder='big', signed=True)
            rx_data = rx_data[4:]

        # temperature,加头共4byte
        if ((0x02 == rx_data[0]) and (0x67 == rx_data[1])):

            int_temperature = int.from_bytes(rx_data[2:4], byteorder='big', signed=True)
            float_temperature = int_temperature * 0.1
            print('temperature:%.2f' % float_temperature)
        try:
            print('van 0000')
            rak_node_test.insert_node_data(dev_eui, int_humidity, int_temperature)
            print('van 0001_1')
            print(global_curent_dev_eui)
            print(dev_eui)
            print('global_curent_dev_eui:%s, dev_eui:%s' % (global_curent_dev_eui, dev_eui))
            if (global_curent_dev_eui == dev_eui):
                print('van 00002')
                data_tuple = rak_node_test.select_node_data(global_dev_index, 1)
                print(len(data_tuple))
                blynk_send_last_seen(data_tuple[0][0])
                blynk_send_last_humidity(data_tuple[0][1])
                blynk_send_last_temperature(data_tuple[0][2])
                for data_info in data_tuple:
                    blynk_send_one_data_to_terminal(data_info)
        except Exception as e:
            raise e
            print('van 0001')
            print(e)
        finally:
            print('van 000001')
            pass


    def on_subscribe(self):
        self.mqtt_client.subscribe(TOPIC, 1)
        self.mqtt_client.on_message = self.on_message_come

insert_db_test = insert_db_a()
def main():
    try:
#        rak_loraserver_test.set_db_insert_func(insert_node_data)
        insert_db_test.on_subscribe()
        
        while True:
            blynk.run()
            pass
    except Exception as e:
        raise e
    finally:
        pass



if __name__ == '__main__':
    main()

import paho.mqtt.client as mqtt
import json
import base64

TOPIC = "application/#"

def insert_node_data1(dev_eui, humidity, temperature):
    print['insert_node_data1']

class rak_loraserver:
    def __init__(self, server_ip='127.0.0.1', server_port=1883):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(server_ip, server_port)
        self.mqtt_client.loop_start()


    def set_db_insert_func(self, func):
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
#        print('dev_eui:%s lora data.' % dev_eui)
        #    print('base64_decode_data***********************:')
        #    print_hex(rx_data)
        #    print('***********************base64_decode_data:')

        # gps,加头共11byte，不关注，去除抛弃
        if ((0x01 == rx_data[0]) and (0x88 == rx_data[1])):
#            print('[on_message_come] gps')
            rx_data = rx_data[11:]

        # battery，加头共4byte
        if ((0x08 == rx_data[0]) and (0x02 == rx_data[1])):
#            print('[on_message_come] battery')
            int_voltage = int.from_bytes(rx_data[2:4], byteorder='big', signed=True)  ##signed标志是否为有符号数
            float_voltage = int_voltage * 0.01
            rx_data = rx_data[4:]
        #        print('battery:%f' % float_voltage)
        #    print('after battery***********************:')
        #    print_hex(rx_data)
        #    print('***********************after battery:')

        # Acceleration，加头共8byte，不关注，抛弃
        if ((0x03 == rx_data[0]) and (0x71 == rx_data[1])):
#            print('[on_message_come] Acceleration')
            rx_data = rx_data[8:]
        #    print('[on_message_come] 001')
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
            float_humidity = int_humidity * 0.5
#            print('humidity:%.2f' % float_humidity)
#            ada_send_humidity(app_name, dev_eui, float_humidity)
            rx_data = rx_data[3:]

        # pressure,加头共4byte
        if ((0x06 == rx_data[0]) and (0x73 == rx_data[1])):
            #        print('[on_message_come] pressure')
            int_pressure = int.from_bytes(rx_data[2:4], byteorder='big', signed=True)
            float_pressure = int_pressure * 0.1
            rx_data = rx_data[4:]
        #    print('[on_message_come] 002')
        # temperature,加头共4byte
        if ((0x02 == rx_data[0]) and (0x67 == rx_data[1])):
#            print('[on_message_come] temperature')
            int_temperature = int.from_bytes(rx_data[2:4], byteorder='big', signed=True)
            float_temperature = int_temperature * 0.1
            print('temperature:%.2f' % float_temperature)
#            ada_send_temperature(app_name, dev_eui, float_temperature)

    def on_subscribe(self):
        self.mqtt_client.subscribe(TOPIC, 1)
        self.mqtt_client.on_message = self.on_message_come

def main():
    rak_loraserver_test = rak_loraserver('127.0.0.1', 1883, insert_node_data1)
#    rak_loraserver_test.set_db_insert_func(insert_node_data1)

    while True:
        rak_loraserver_test.on_subscribe()
        pass


if __name__ == '__main__':
    main()
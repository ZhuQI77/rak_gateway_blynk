import psycopg2
#import redis

class rak_db:
    _node_eui_list = []
    def __init__(self):
        try:
#            self._redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
            self._as_conn = psycopg2.connect(database="loraserver_as", user="rak_blynk", password="rak_blynk",
                                            host="192.168.6.90", port="5432")
            self._blynk_conn = psycopg2.connect(database="rak_blynk", user="rak_blynk", password="rak_blynk",
                                            host="192.168.6.90", port="5432")
        except Exception as e:
            print(e)
            exit(-1)
            pass
        finally:
            pass

    def get_nodes(self):
        cur = self._as_conn.cursor()
        try:
            self._node_eui_list.clear()
            cur.execute("SELECT encode(dev_eui::bytea,'hex') FROM device")
            rows = cur.fetchall()
            for row in rows:
                self._node_eui_list.append(row[0])
        except Exception as e:
            print(e)
        finally:
            cur.close()

        return tuple(self._node_eui_list)

    def insert_node_data(self, dev_eui, humidity, temperature):
        print('insert_node_data')
        cur = self._blynk_conn.cursor()
        try:
            cur.execute("INSERT INTO log_node  (dev_eui, create_at, humidity, temperature ) VALUES(\'%s\', NOW(), %d, %d)"
                        % (dev_eui, humidity, temperature))
            self._blynk_conn.commit()
        except Exception as e:
            raise e
            print(e)
        finally:
            cur.close()

    def select_node_data(self, dev_eui_index, data_num=10):
        node_data = []
        cur = self._blynk_conn.cursor()

        try:
            cur.execute("SELECT  to_char(create_at, 'yyyy-mm-dd hh24:mi:ss'), humidity, temperature FROM log_node WHERE dev_eui=\'%s\' ORDER BY log_id DESC LIMIT %d OFFSET 0" % (self._node_eui_list[dev_eui_index], data_num))
            rows = cur.fetchall()
            for row in rows:
                info_list = []
                info_list.append(row[0])
                info_list.append(row[1])
                info_list.append(row[2])
                node_data.append(info_list)
        except Exception as e:
            raise e
        finally:
            cur.close()
        node_data.reverse()
        return node_data

    def get_node_dev(self, dev_index):
        return self._node_eui_list[dev_index]

def main():
    rak_node_test = rak_db()
    print(rak_node_test.select_node_data('1122334455667788'))



if __name__ == '__main__':
    main()

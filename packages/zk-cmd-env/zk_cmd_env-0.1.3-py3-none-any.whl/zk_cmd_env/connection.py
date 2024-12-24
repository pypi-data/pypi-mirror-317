import os
import time
import socket
import json
import io
import zipfile

class Connection:

    def __init__(self, env_args):
        self.args = env_args
        self.excute_cmd = f'{self.args.excute_path} Ip={self.args.ip} Port={self.args.port} PlayMode={self.args.play_mode} RedNum={self.args.red_num} BlueNum={self.args.blue_num} Red={self.args.red_com} Blue={self.args.blue_com} Scenes={self.args.scenes}'
        self.create_entity()
        self.unity = None
        self.data = None

    def create_entity(self):
        is_success = False
        while not is_success:
            try:
                print('Creating Env', self.excute_cmd)
                self.unity = os.popen(self.excute_cmd)
                time.sleep(20)
                self._connect()
                is_success = True
                print('Env Created')
            except Exception as e:
                print('Create failed and the reason is ', e)
                time.sleep(5)

    def _connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(50)
        print(f'Connecting {self.args.ip}:{self.args.port}')
        self.socket.connect((self.args.ip, self.args.port))

    def send_condition(self, data_dict):
        data = json.dumps(data_dict)
        self.data = data
        self.socket.send(bytes(data.encode('utf-8')))

    def accept_from_socket(self):
        load_data = None
        try:
            load_data = self.socket.recv(8192 * 16)
            zip_data = io.BytesIO(load_data)
            zip_file = zipfile.ZipFile(zip_data)
            msg_receive = zip_file.read(zip_file.namelist()[0])
            msg_receive = json.loads(str(msg_receive, encoding='utf-8'))
        except Exception as e:
            if e == socket.timeout:
                print('out of time')
            print("fail to recieve message from unity")
            print('load_data', load_data)
            print("the last sent data is: ", self.data)
            print(e)
            self.send_condition(self.data)
            load_data = self.socket.recv(8192 * 16)
            zip_data = io.BytesIO(load_data)
            zip_file = zipfile.ZipFile(zip_data)
            msg_receive = zip_file.read(zip_file.namelist()[0])
            msg_receive = json.loads(str(msg_receive, encoding='utf-8'))
        return msg_receive
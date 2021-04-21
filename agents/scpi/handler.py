import socket
import time
import pandas as pd
import json
timeout = 1 # timeout len used in connection
port = 5025 # port used for connection
buf_sz = 1024 # size of buffer used in recv

class SCPI:
    def __init__(self,addr = "127.0.0.1",commands_file='scpi/commands.json',log_file='log'):
        '''
            params:
                * addr: address of server to connect to
                * commands_file: path to SCPI commands file
                * log_file: desired name of log file
            return:
                None
        '''
        self.addr = addr
        self.soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.soc.settimeout(timeout) # time out in secs
        self.soc.connect((addr,port))
        with open(commands_file,'r') as f:
            commands = json.load(f)
        self.commands = commands
        self.log_file = log_file+'.csv'
        return
    def log(self,l):
        l['time'] = int(time.time()) 
        print(l)
        df = pd.DataFrame(l)
        df.set_index('time',inplace=True)
        df.to_csv(self.log_file,mode='a',header=False)
        return

    def send_command(self,cmd):
        '''
            sends a command through the socket
        '''
        self.soc.send(cmd.encode())
        ret = self.soc.recv(buf_sz)
        return ret.decode()

    # ================= common commands functions ================
    # def lock_screen(self):
    #     '''
    #         params:
    #             None
    #         return:
    #             * servers response to scpi command
    #     '''
    #     # lock screen
    #     return self.send_command(self.commands['common']['lock screen'])
    # =================
    # def clear_status(self):
    #     return self.send_command(self.commands['common']['clear status'])
    # # =================
    # def event_status_enable(self):
    #     return self.send_command(self.commands['common']['event status enable'])
    # # =================
    # def event_status_register(self):
    #     return self.send_command(self.commands['common']['clear status'])
    # # =================
    # def clear_status(self):
    #     return self.send_command(self.commands['common']['clear status'])
    def send(self,cmd):
        status = False
        try:
            cmd = self.commands['common'][cmd]
            res = self.send_command(cmd) # send command 
            # self.send_command('QUIT')
            status = True
        except Exception as e:
            res = e
        self.log({'command':[cmd],'response':[res],'status':[status]})
        return (status,res)
    # ================= other commands functions ================